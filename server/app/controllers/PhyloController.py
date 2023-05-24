from models.persist.PhyloDao import PhyloDao 
from models.persist.FastaDao import FastaDao
from models.persist.MultiFastaDao import MultiFastaDao
from models.PhyloTree import PhyloTree
from models.Fasta import Fasta
from pathlib import Path

from Bio import AlignIO
from Bio.Align.Applications import ClustalOmegaCommandline
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio import Phylo
from Bio.Phylo.PhyloXML import Phylogeny
import re

import subprocess
from multiprocessing import Process
import os
import signal
from uuid import uuid4
from shutil import rmtree

active_threads: dict[Process] = {}
active_subprocess: dict[int] = {}
temporal_folders: dict[Path] = {}

class PhyloController:
    
    def __init__(self) -> None:
        self.dao: PhyloDao = PhyloDao()
        self.fasta_dao: FastaDao = FastaDao()
        self.multi_fasta_dao: MultiFastaDao = MultiFastaDao()
        
        
    async def get_phylo_by_id(self, fasta_id: int) -> dict[str, str]:
        """Returns a phylo entry identified by the given id

        Args:
            fasta_id (int): The fasta id of the desired phylo

        Returns:
            list[str]:  If found, returns the phylo in a list.
        """

        phyloTree: dict[str, str] = []

        try:
            listPhyloTree = self.dao.get_phylo_by_fasta_id(fasta_id)
            
            phyloTree = {"fasta_id": listPhyloTree[0].get_fasta_id(), "tree": listPhyloTree[0].get_newick()}
            
        except Exception as e:
            print(f"PhyloController Exception: {e}")

        return phyloTree
    
    def parse_fasta_to_phylo(self, fasta: Fasta) -> bool:
        """Takes a Fasta object and parses it into a Newick, to construct a phylogenetic tree (by calling the do_clustalo_alignment function in another thread)

        Args:
            fasta (Fasta): A Fasta object

        Returns:
            bool: Indicates if the process is running or not
        """
        
        is_processing = False
        
        try:
            thread = Process(target=PhyloController.do_clustalo_alignment, args=(fasta.get_id(),fasta.get_raw_fasta(), fasta.get_user_id()))
            thread.start()
            
            active_threads[fasta.get_id()] = thread
            
            if thread.is_alive():
                is_processing = True 
            
        except Exception as e:
            self.multi_fasta_dao.delete_multi(fasta.get_id())
            self.fasta_dao.delete_fasta(fasta.get_id())
            print(f"Error on parse fasta to phylo controller: {e}")
        
        return is_processing
    
    def save_phylo(self, phylo: PhyloTree) -> int:
        """Add a new PhyloTree to database

        Args:
            phylo (PhyloTree): The new PhyloTree to add to the database

        Returns:
            int: The number of rows added to the table
        """
        
        saved_rows: int = 0
        try:
            response = self.dao.insert_phylo(phylo)
            saved_rows = response
            
        except Exception as e:
            print(f"Save phylo Newick controller error: {e}")
            
        return saved_rows


    # ----------------------------------------------------------------
    # Validate Multifasta
    async def validate_multifasta(self, multi_fasta):
        """Validates that a fasta is multi as opposed to single

        Args:
            multi_fasta (_type_): The fasta to validate

        Returns:
            bool: A bool indicating if the fasta is multi or not
        """
        
        is_correct: bool = False

        # Validates that the file is a valid multifasta format
        if multi_fasta.count(">") > 1 and multi_fasta.count(">") < 50:
            is_correct = True

        # Valida que las secuencias son nucleótidos
        if re.search(r'[^ATCGatcg\n]+', multi_fasta) and is_correct:
            is_correct = True

        return is_correct
    
    # ------------------------------------------------------

    async def del_phylo(self, fasta_id) -> int:
        """Removes a phylo from the database

        Args:
            fasta_id (int): The id of the fasta to which the phylo to delete belongs

        Returns:
            int: A code from the list indicating if the operation was successful, or what failed exactly
        """

        try:
            phylo_deleted = self.dao.delete_phylo(fasta_id)
            
            if fasta_id in active_threads:
                
                thread = active_threads[fasta_id]
                thread.terminate()
                thread.join()
                
                process = active_subprocess[fasta_id]
                process.kill()
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                
                temporal_path = temporal_folders[fasta_id]
                rmtree(temporal_path)
                
                del active_threads[fasta_id]
                del active_subprocess[fasta_id]
                del temporal_folders[fasta_id]
            
        except Exception as e:
            print(f"Delete phylo Controller: {e}")

        return phylo_deleted
        
    def do_clustalo_alignment(fasta_id: int, fasta_seq: str, fasta_user_id: int):
        """Gets a fasta and calculates the corresponding phylogenetic tree

        Args:
            fasta_id (int): The fasta's id
            fasta_seq (str): The fasta's sequence
            fasta_user_id (int): The fasta's user's id

        Raises:
            Exception: Raised if there's an exception
        """
        
        temp_dir = Path(f"/temporal")
        temp_dir.mkdir(exist_ok=True)
        
        temporal_path = temp_dir/str(uuid4())
        temporal_path.mkdir()
        
        
        try:
            fasta_content = fasta_seq
            
            input_fasta_path = temporal_path/"fasta.fasta"
            output_fasta_path = temporal_path/"output.fasta"
            phylo_file_path = temporal_path/"phylo.nwk"
            
            with open(input_fasta_path, "w+") as input_file:
                input_file.write(fasta_content)
                
                    
            clustalo_cline = ClustalOmegaCommandline(
                                infile = input_fasta_path.absolute(),
                                outfile = output_fasta_path.absolute(),
                                threads = 1,
                                seqtype = "DNA",
                                max_guidetree_iterations = 1,
                                max_hmm_iterations=10,
                                iterations=1,
                                distmat_full=False,
                                distmat_full_iter=False,
                                usekimura=False,
                                force=True,
                                outfmt="fasta"
                                )
        
            cmd_string = str(clustalo_cline)
            
            nice_cmd = f"nice -n 19 {cmd_string}"
                
            process = subprocess.Popen(nice_cmd, 
                                        shell=True, 
                                        preexec_fn=os.setsid, 
                                        stdin=subprocess.PIPE, 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.STDOUT)
            
            temporal_folders[fasta_id] = temporal_path
            active_subprocess[fasta_id] = process
            process.communicate()
                
            alignment_file_path = list(temporal_path.glob("output.fasta"))
                
            if len(alignment_file_path) == 1:
                alignment_file_path = alignment_file_path[0]
            else:
                raise Exception("Incorrect alignment")
            
            clustal_alignment = AlignIO.read(alignment_file_path, "fasta")
        
            calcultaor = DistanceCalculator("identity")
            distance_matrix = calcultaor.get_distance(clustal_alignment)
            
            tree_constructor = DistanceTreeConstructor()
            phylo_tree = tree_constructor.upgma(distance_matrix)
            phylo_newick= Phylogeny.from_tree(phylo_tree)
            
            with open(phylo_file_path, "w") as phylo_file:
                Phylo.write(phylo_newick,phylo_file,"newick")
                
            phylo_newick_str = ""
            with open(phylo_file_path, "r") as newick:
                phylo_newick_str = newick.read() 
                
            phylo = PhyloTree(fasta_id,
                            fasta_user_id,
                            phylo_newick_str)
            
            PhyloController().save_phylo(phylo)
                
        except Exception as e:
            PhyloController().multi_fasta_dao.delete_multi(fasta_id)
            PhyloController().fasta_dao.delete_fasta(fasta_id)
            try:
                del active_threads[fasta_id]
                del active_subprocess[fasta_id]
                del temporal_folders[fasta_id]
            except:
                pass
            print(f"Error on ClustalO: {e}")
        finally:
            rmtree(temporal_path)
        
