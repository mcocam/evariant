# from models.persist.FastaDao import FastaDao
from models.persist.SingleFastaDao import SingleFastaDao
from models.Fasta import Fasta
from models.SingleFasta import SingleFasta


class SingleFastaController:
    def __init__(self) -> None:
        self.dao = SingleFastaDao()

    def parse_single_fasta(self, fasta: Fasta) -> int:
        """Parses a Fasta into a SingleFasta and adds it to the db

        Args:
            fasta (Fasta): A Fasta object

        Returns:
            int: The id assigned to the newly addes singlefasta
        """
        
        inserted_id: int = 0
        
        try:
            raw = fasta.get_raw_fasta()
            
            seq = "".join(raw.split("\n")[1:])
            seq = seq.replace(" ", "").replace("\t", "")
            

            first_line = raw.split('\n')[0][1:]
            sections = first_line.split(';')    # assembly;chromosome;strand;positions;
            positions = sections[3].split(":")

            sf = SingleFasta(fasta.get_id(), seq.upper(), sections[0], sections[1], sections[2], positions[0], positions[1])

            inserted_id: int = self.dao.add_new_single_fasta(sf)
        except Exception as e:
            print(f"Parse single fasta to DB controller: {e}")
            
        return inserted_id
    
    async def get_single_fasta_by_id(self, id: int) -> SingleFasta or None:
        """Returns the SingleFasta identified by the given id

        Args:
            id (int): The id number of the desired fasta

        Returns:
            SingleFasta: A SingleFasta object
        """
        
        data = None

        try:
            result = await self.dao.get_single_fasta_by_id(id)
            data = result["data"]

        except Exception as e:
            print(f"Get fasta info error: {e}")

        return data

    async def del_single(self, fasta_id) -> int:
        """Removes a single fasta from the database

        Args:
            fasta_id (int): The id of the fasta to delete

        Returns:
            int: A code from the list indicating if the operation was successful, or what failed exactly
        """

        try:
            single_deleted = self.dao.delete_single(fasta_id)
        except Exception as e:
            single_deleted = e

        return single_deleted