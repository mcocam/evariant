
class MultiFasta:

    def __init__(self,
                 fasta_id:      int
                 ) -> None:
        
        self.fasta_id = fasta_id

    # GETTERS
    def getFastaId(self) -> int:
        return self.fasta_id

    # SETTERS
    def setFastaId(self, f_id: int) -> None:
        self.fasta_id = f_id


