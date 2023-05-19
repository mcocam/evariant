from models.persist.PhyloDao import PhyloDao 
from models.persist.FastaDao import FastaDao
from models.persist.MultiFastaDao import MultiFastaDao
from models.PhyloTree import PhyloTree
from models.Fasta import Fasta
from tempfile import TemporaryDirectory
from pathlib import Path

from Bio import AlignIO
from Bio.Align.Applications import ClustalOmegaCommandline
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio import Phylo
from Bio.Phylo.PhyloXML import Phylogeny
import re

import subprocess
import threading


class PhyloController:
    
    def __init__(self) -> None:
        self.dao: PhyloDao = PhyloDao()
        self.fasta_dao: FastaDao = FastaDao()
        self.multi_fasta_dao: MultiFastaDao = MultiFastaDao()
        
    async def get_phylo_by_id(self, fasta_id: int) -> dict[str, str]:

        phyloTree: dict[str, str] = []

        try:
            listPhyloTree = self.dao.get_phylo_by_fasta_id(fasta_id)
            
            phyloTree = {"fasta_id": listPhyloTree[0].get_fasta_id(), "tree": listPhyloTree[0].get_newick()}
            
        except Exception as e:
            print(f"PhyloController Exception: {e}")

        return phyloTree
    
    def parse_fasta_to_phylo(self, fasta: Fasta) -> bool:
        
        is_processing = False
        
        thread = threading.Thread(target=PhyloController.do_clustalo_alignment, args=(self, fasta))
        thread.start()
        
        if thread.is_alive():
            is_processing = True 
        
        return is_processing
    
    def save_phylo(self, phylo: PhyloTree) -> int:
        
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
        
        is_correct: bool = False

        # Validates that the file is a valid multifasta format
        if multi_fasta.count(">") > 1:
            is_correct = True

        # Valida que las secuencias son nucleótidos
        if re.search(r'[^ATCGatcg\n]+', multi_fasta) and is_correct:
            is_correct = True

        return is_correct
    
    # ------------------------------------------------------

    async def del_phylo(self, fasta_id) -> int:

            try:
                phylo_deleted = self.dao.delete_phylo(fasta_id)
                
            except Exception as e:
                print(e)

            return phylo_deleted
        
    async def do_clustalo_alignment(self, fasta: Fasta):
        
        
        try:
            fasta_content = fasta.get_raw_fasta()
        
            with TemporaryDirectory() as temp_dir:
        
                temp_dir_path: Path = Path(temp_dir)
                
                fasta_file_path = temp_dir_path/"fasta.fasta"
                phylo_file_path = temp_dir_path/"phylo.nwk"
                
                with open(fasta_file_path, "w") as fasta_file:
                    fasta_file.write(fasta_content)
                    
                clustalo_cline = ClustalOmegaCommandline(
                                        infile = temp_dir_path/"fasta.fasta",
                                        outfile = temp_dir_path/"output.fasta",
                                        threads = 2,
                                        seqtype = "DNA",
                                        max_guidetree_iterations = 1,
                                        max_hmm_iterations=100,
                                        iterations=1
                                        )
                
                cmd_string = str(clustalo_cline)

                nice_cmd = f"nice -n 19 {cmd_string}"
                    
                subprocess.run(nice_cmd, shell=True)
                    
                alignment_file_path = list(temp_dir_path.glob("output.fasta"))
                    
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
                    
                phylo = PhyloTree(fasta.get_id(),
                                fasta.get_user_id(),
                                phylo_newick_str)
                
                self.save_phylo(phylo)
                    
        except Exception as e:
            await self.multi_fasta_dao.delete_multi(fasta.get_id())
            await self.fasta_dao.delete_fasta(fasta.get_id())
            print(f"Error on ClustalO: {e}")
        
