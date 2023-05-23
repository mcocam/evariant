from models.persist.MultiFastaDao import MultiFastaDao
from models.Fasta import Fasta
from models.MultiFasta import MultiFasta

class MultiFastaController:
    
    def __init__(self) -> None:
        self.dao: MultiFastaDao = MultiFastaDao()
        
    async def insert_fasta(self, fasta: Fasta) -> int:
        """Add a new multifasta to the database

        Args:
            fasta (Fasta): A Fasta object

        Returns:
            int: The id assigned to the newly added multifasta
        """
        
        new_fasta_added: int = 0

        try:
            new_multi_fasta: MultiFasta = MultiFasta(fasta.get_id())
            new_fasta_added = self.dao.insert_fasta_id(new_multi_fasta)
        except Exception as e:
            print(f"Insert in multifasta controller: {e}")

        return new_fasta_added
    

    async def del_multi(self, fasta_id) -> int:
        """Removes a fasta from the database

        Args:
            fasta_id (int): The id of the fasta to delete

        Returns:
            int: A code from the list indicating if the operation was successful, or what failed exactly
        """

        try:
            multi_deleted = self.dao.delete_multi(fasta_id)
        except Exception as e:
            multi_deleted = e

        return multi_deleted