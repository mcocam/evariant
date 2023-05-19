# Class Snp
# @author: Melania Prado

from datetime import datetime

class Snp:

    def __init__(self,
                 ref_snp: str,
                 fasta_id: int,
                 ref_nucleotide: str,
                 var_nucleotide: str,
                 id: int = None,
                 creation_date: datetime = None
                 ) -> None:
        
        self.id: int = id
        self.ref_snp: str = ref_snp
        self.fasta_id: int = fasta_id
        self.ref_nucleotide: str = ref_nucleotide
        self.var_nucleotide: str = var_nucleotide
        self.creation_date: datetime = creation_date

    # GETTERS
    def get_ref_snp(self) -> str:
        return self.ref_snp
    
    def get_fasta_id(self) -> int:
        return self.fasta_id
    
    def get_id(self) -> int:
        return self.id
    
    def get_ref_nucleotide(self) -> str:
        return self.ref_nucleotide
    
    def get_var_nucleotide(self) -> str:
        return self.var_nucleotide
    
    def get_creation_date(self) -> datetime:
        return self.creation_date
    
    # SETTERS
    def set_ref_snp(self, ref_snp: str) -> None:
        self.ref_snp = ref_snp

    def set_fasta_id(self, fasta_id: int) -> None:
        self.fasta_id = fasta_id

    def set_id(self, id: int) -> None:
        self.id = id

    def set_ref_nucleotide(self, ref_nucleotide: str) -> None:
        self.ref_nucleotide = ref_nucleotide
    
    def set_var_nucleotide(self, var_nucleotide: str) -> None:
        self.var_nucleotide = var_nucleotide
