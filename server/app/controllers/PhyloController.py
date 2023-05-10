from models.persist.PhyloDao import PhyloDao
from models.PhyloTree import PhyloTree
from models.Fasta import Fasta
from tempfile import TemporaryDirectory
from pathlib import Path

from Bio import AlignIO
from Bio.Align.Applications import ClustalwCommandline
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio import Phylo
from Bio.Phylo.PhyloXML import Phylogeny
import re

class PhyloController:
    
    def __init__(self) -> None:
        self.dao: PhyloDao = PhyloDao()
        
    async def get_phylo_by_id(self, fasta_id: int) -> dict[str, str]:

        phyloTree: dict[str, str] = []

        try:
            listPhyloTree = self.dao.get_phylo_by_fasta_id(fasta_id)
            
            phyloTree = {"fasta_id": listPhyloTree[0].get_fasta_id(), "xml": listPhyloTree[0].get_xml()}
            
        except Exception as e:
            print(f"PhyloController Exception: {e}")

        return phyloTree
    
    async def parse_fasta_to_phylo(self, fasta: Fasta) -> PhyloTree | None:
        
        phylo = None
        
        try:
            fasta_content = fasta.get_raw_fasta()
        
            with TemporaryDirectory() as temp_dir:
        
                temp_dir_path: Path = Path(temp_dir)
                
                fasta_file_path = temp_dir_path/"fasta.fasta"
                phylo_file_path = temp_dir_path/"phylo.xml"
                
                with open(fasta_file_path, "w") as fasta_file:
                    fasta_file.write(fasta_content)
                    
                with open(fasta_file_path, "r") as fasta_file:

                    clustalw_cline = ClustalwCommandline("clustalw",
                                                    infile = fasta_file.name,
                                                    bootstrap = 10,
                                                    ktuple = 2,
                                                    pairgap = 3,
                                                    align = True,
                                                    quiet = True)
                    stdout, stderr = clustalw_cline()
                    
                    alignment_file_path = list(temp_dir_path.glob("*.aln"))

                    
                    if len(alignment_file_path) == 1:
                        alignment_file_path = alignment_file_path[0]
                    else:
                        #return
                        print("Error")
                
                    clustal_alignment = AlignIO.read(alignment_file_path, "clustal")
                
                    calcultaor = DistanceCalculator("identity")
                    distance_matrix = calcultaor.get_distance(clustal_alignment)
                    
                    tree_constructor = DistanceTreeConstructor()
                    phylo_tree = tree_constructor.upgma(distance_matrix)
                    phylo_xml= Phylogeny.from_tree(phylo_tree).as_phyloxml()
                    
                    with open(phylo_file_path, "w") as phylo_file:
                        Phylo.write(phylo_xml,phylo_file,"phyloxml")
                        
                    phylo_xml_str = ""
                    with open(phylo_file_path, "r") as xml:
                        phylo_xml_str = xml.read() 
                        
                    phylo = PhyloTree(fasta.get_id(),
                                    fasta.get_user_id(),
                                    phylo_xml_str)
                    
        except Exception as e:
            print(f"Error on parse fasta to Phylo Controller: {e}")
        
        return phylo
    
    def save_phylo_xml(self, phylo: PhyloTree) -> int:
        
        saved_rows: int = 0
        try:
            response = self.dao.insert_phylo(phylo)
            saved_rows = response
            
        except Exception as e:
            print(f"Save phylo XML controller error: {e}")
            
        return saved_rows
    
    async def remove_phylos(self, fastas_id: list[Fasta]) -> int:
        pass 

    # ----------------------------------------------------------------
    # Validate Multifasta
    async def validate_multifasta(self, multi_fasta):

        # Validates that the file is a valid multifasta format
        if not re.search(r'^>[^\n]+\n[ATCGatcg\n]+$', multi_fasta, flags=re.MULTILINE):
            return False

        # Valida que las secuencias son nucleótidos
        if re.search(r'[^ATCGatcg\n]+', multi_fasta):
            return False

        return 0
    
    # ------------------------------------------------------