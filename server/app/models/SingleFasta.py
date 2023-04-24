# Class SingleFasta
# @author: Marc Garcia

from datetime import datetime

class SingleFasta:

    def __init__(self,
                 fasta_id:      int,
                 assembly:      str,
                 chromosome:    str,
                 strand:        int,
                 start_loc:     int,
                 end_loc:       int,
                 ) -> None:
        
        self.fasta_id = fasta_id
        self.assembly = assembly
        self.chromosome = chromosome
        self.strand     = strand
        self.start_loc = start_loc
        self.end_loc = end_loc

    # GETTERS
    def getFastaId(self) -> int:
        return self.fasta_id
    
    def getAssembly(self) -> str:
        return self.assembly

    def getChromosome(self) -> str:
        return self.chromosome

    def getStartLoc(self) -> int:
        return self.start_loc
    
    def getEndLoc(self) -> int:
        return self.end_loc

    # SETTERS
    def setFastaId(self, f_id: int) -> None:
        self.fasta_id = f_id

    def setAssembly(self, asmb: str) -> None:
        self.assembly = asmb

    def setChromosome(self, chr: str) -> None:
        self.chromosome = chr

    def setStartLoc(self, start_l: int) -> None:
        self.start_loc = start_l

    def setEndLoc(self, end_l: int) -> None:
        self.end_loc = end_l


