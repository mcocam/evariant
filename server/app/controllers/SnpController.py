# Class Snp
# @author: Melania Prado

from models.persist.SnpDao import SnpDao
from models.Snp import Snp

class SnpController:
    
    def __init__(self):
        self.dao = SnpDao()
    
    # ----------------------------------------------------------------
    async def create_snp(self, snp: Snp) -> bool:

        """
        Creates a new SNP in the database.

        Args:
            snp: An instance of the Snp model.

        Returns:
            A boolean indicating if the SNP was successfully created in the database.
        """

        result: bool = False

        try:
            result = self.dao.add_new_snp(snp)

        except Exception as e:
            print(f"create_snp: {e}")

        return result
    


    # ----------------------------------------------------------------
    async def get_snp_by_id(self, id: int) -> Snp:

        """
        Retrieves an SNP from the database by its ID.

        Args:
            id: An integer representing the ID of the SNP to retrieve.

        Returns:
            An instance of the Snp model.
        """

        snp: Snp = Snp()

        try:
            snp = self.dao.get_snp_by_id(id)

        except Exception as e:
            print(f"get_snp_by_id: {e}")

        return snp
    

    # ----------------------------------------------------------------
    async def get_snps_by_fasta_id(self, fasta_id: int) -> list[Snp]:

        """
        Retrieves all SNPs from the database associated with a given FASTA ID.

        Args:
            fasta_id: An integer representing the ID of the FASTA to retrieve SNPs for.

        Returns:
            A list of instances of the Snp model.
        """

        fasta_snps: list[Snp] = []
        
        try:
            fasta_snps = await self.dao.get_snps_by_fasta_id(fasta_id)

        except Exception as e:
            print(f"get_snps_by_fasta_id: {e}")

        return fasta_snps



# ----------------------------------------------------------------
    async def get_snp_refs_by_fasta_id(self, fasta_id: int) -> list[str]:

        """
        Retrieves all SNPs references from the database associated with a given FASTA ID.

        Args:
            fasta_id: An integer representing the ID of the FASTA to retrieve SNPs for.

        Returns:
            A list of SNP references (string)
        """

        fasta_snps_refs: list[str] = []
        
        try:
            fasta_snps_refs = await self.dao.get_snp_refs_by_fasta_id(fasta_id)

        except Exception as e:
            print(f"get_snp_refs_by_fasta_id: {e}")

        return fasta_snps_refs





    async def save_snps_to_db(self, snp: Snp) -> bool:
        """
        Retrieves SNPs from a FASTA file by a list of positions and saves them to the database.
        
        Args:
        - fasta_id: An integer representing the ID of the FASTA file to retrieve SNPs from.
        - positions: A list of integers representing the positions to retrieve SNPs for.
        
        Returns:
        - A boolean indicating if the SNPs were successfully saved to the database.
        """

        
        # Retrieve SNPs from the FASTA file by positions
        
        # Save SNPs to the database
        response = await self.dao.add_new_snp(snp)
        
        return response
    
    async def del_snp(self, fasta_id) -> int:

        try:
            snp_deleted = self.dao.delete_snp(fasta_id)
        except Exception as e:
            print(e)

        return snp_deleted