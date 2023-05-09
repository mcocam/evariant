from models.persist import PhyloDao
from models.PhyloTree import PhyloTree
from models.Fasta import Fasta
from tempfile import TemporaryFile
from uuid import uuid4

from Bio import AlignIO
from Bio.Align.Applications import ClustalwCommandline
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio import Phylo
from Bio.Phylo.PhyloXML import Phylogeny

class PhyloController:
    
    def __init__(self) -> None:
        self.dao: PhyloDao = PhyloDao()
        self.temp_fasta = TemporaryFile()
        self.temp_
        
    def get_phylo_by_id(self, fasta_id: int) -> list[PhyloTree]:
        pass
    
    def parse_fasta_to_phylo(self, fasta: Fasta):
        pass
    
    def remove_phylos(self, fastas_id: list[Fasta]) -> int:
        pass 