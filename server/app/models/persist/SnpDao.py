# Class SnpDao.py
# @author: Melania Prado

from models.Snp import Snp
from db.get_connection import get_connection
from sqlalchemy import Table, MetaData, Column, Integer, String, insert, select
from typing import List
from datetime import datetime


snps_table_model: Table = Table(
    "snps",
    MetaData(),
    Column("id", Integer, primary_key=True, autoincrement='auto'),
    Column("ref_snp", String, unique=True),
    Column("fasta_id", Integer),
    Column("ref_nucleotide", String),
    Column("var_nucleotide", String)
)

class SnpDao:
    """
    This class contains the CRUD operations for SNPs.
    """
    def __init__(self) -> None:
        self.connection = get_connection()
        self.snp_table = snps_table_model

    # ----------------------------------------------------------------
    async def get_snp_by_id(self, id: int) -> Snp:
        """
        Retrieves a SNP by its id from the database.
        
        Arguments:
        - id: The id of the SNP to retrieve.
        
        Returns:
        - A Snp object containing the data from the row, or None if not found.
        """
        query = select([self.snp_table]).where(self.snp_table.c.id == id)
        cursor = self.connection.connect()
        rows = cursor.execute(query)
        data = rows.fetchone()
        if data:
            snp = self.__parse_snp(data)
            return snp
        else:
            return None


    # ----------------------------------------------------------------
    async def get_snps_by_fasta_id(self, fasta_id: int) -> List[Snp]:
        """
        Retrieves all the SNPs for a given FASTA id from the database.
        
        Arguments:
        - fasta_id: The id of the FASTA to retrieve SNPs for.
        
        Returns:
        - A list of Snp objects containing the data from each row, or an empty list if none found.
        """
        snps = []
        query = self.snp_table.select().where(self.snp_table.c.fasta_id == fasta_id)

        cursor = self.connection.connect()
        rows = cursor.execute(query)
        for row in rows:
            snp = await self.__parse_snp(row)
            snps.append(snp)
        return snps
    

    # ----------------------------------------------------------------
    async def add_new_snp(self, snp: Snp) -> bool:
        """
        Adds a new SNP to the database.
        
        Arguments:
        - snp: A Snp object containing the data for the new SNP.
        
        Returns:
        - True if the SNP was added successfully, False otherwise.
        """
        
        inserted_rows: int = 0
        
        new_snp_added = False
        query = insert(self.snp_table).values(
            ref_snp=snp.ref_snp,
            fasta_id=snp.fasta_id,
            ref_nucleotide=snp.ref_nucleotide,
            var_nucleotide=snp.var_nucleotide
        )
        try:
            cursor = self.connection.connect()
            response = cursor.execute(query)
            cursor.commit()
            if response.rowcount > 0:
                inserted_rows = response.rowcount
        except Exception as e:
            print(e)
        return inserted_rows


    # ----------------------------------------------------------------
    @staticmethod
    async def __parse_snp(raw_data: List[any]) -> Snp:
        """
        Parses the raw data of a SNP record and creates a Snp object.

        Args:
        - raw_data: a list of raw data values for a single SNP record in the SNPs table.

        Returns:
        - A Snp object containing the parsed data.

        Raises:
        - ValueError if the input data is invalid or missing any required fields.
        """

        if len(raw_data) < 5:
            raise ValueError("Input data is missing required fields.")
        
        snp_id: int = raw_data[0]
        ref_snp: str = raw_data[1]
        fasta_id: int = raw_data[2]
        ref_nucleotide: str = raw_data[3]
        var_nucleotide: str = raw_data[4]
        
        return Snp(snp_id, ref_snp, fasta_id, ref_nucleotide, var_nucleotide)
    
    # ----------------------------------------------------------------
    def delete_snp(self, fasta_id: int) -> int:
        """Removes an snp from the database

        Args:
            fasta_id (int): The id of the fasta to delete

        Returns:
            int: A code from the list indicating if the operation was successful, or what failed exactly
        """

        snp_deleted: int = 0

        query = self.snp_table.delete().where(
            self.snp_table.c.fasta_id == fasta_id
        )

        try:
            cursor = self.connection.connect()
            response = cursor.execute(query)
            cursor.commit()

            if (response.rowcount <= 0):
                snp_deleted = 900

        except Exception as e:
            snp_deleted = e

        return snp_deleted