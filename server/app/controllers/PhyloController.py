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
import re

class PhyloController:
    
    def __init__(self) -> None:
        # self.dao: PhyloDao = PhyloDao()
        self.temp_fasta = TemporaryFile()
        # self.temp_
        
    async def get_phylo_by_id(self, fasta_id: int) -> list[PhyloTree]:
        pass
    
    async def parse_fasta_to_phylo(self, fasta: Fasta):
        pass
    
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