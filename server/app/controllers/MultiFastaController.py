from models.persist.MultiFastaDao import MultiFastaDao
from models.Fasta import Fasta
from models.MultiFasta import MultiFasta

class MultiFastaController:
    
    def __init__(self) -> None:
        self.dao: MultiFastaDao = MultiFastaDao()
        
    async def insert_fasta(self, fasta: Fasta) -> int:
        
        new_fasta_added: int = 0

        try:
            new_multi_fasta: MultiFasta = MultiFasta(fasta.get_id())
            new_fasta_added = self.dao.insert_fasta_id(new_multi_fasta)
        except Exception as e:
            print(f"Insert in multifasta controller: {e}")

        return new_fasta_added