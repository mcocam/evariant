

from models.MultiFasta import MultiFasta
from db.get_connection import get_connection
from sqlalchemy import Engine, Table, MetaData, Column, Integer, String, DateTime, insert
from datetime import datetime

multi_fastas:   Table = Table(
    "multi_fastas",
    MetaData(),
    Column("fasta_id",Integer, primary_key=True)
)

class MultiFastaDao:
    
    def __init__(self) -> None:
        self.connection: Engine = get_connection()
        self.multi_fasta_table: Table = multi_fastas
    
    #----------------------------------------------------------------
    def insert_fasta_id(self, multi_fasta: MultiFasta) -> int:
        """Inserts a new entry to the multifasta table in the database

        Args:
            multi_fasta (MultiFasta): A Multifasta object to be added to de database

        Returns:
            int: The id of the newly added entry
        """
        
        inserted_response: int = 0

        query = insert(self.multi_fasta_table).values(
            fasta_id = multi_fasta.getFastaId()
        )

        try:
            cursor = self.connection.connect()
            response = cursor.execute(query)
            cursor.commit()
            if response.rowcount > 0:
                inserted_response = response.inserted_primary_key[0]

        except Exception as e:
            print(e)

        return inserted_response
    
    #----------------------------------------------------------------
    def delete_multi(self, fasta_id: int) -> int:
        """Removes a fasta from the database

        Args:
            fasta_id (int): The id of the fasta to delete

        Returns:
            int: A code from the list indicating if the operation was successful, or what failed exactly
        """

        multi_deleted: int = 0

        query = self.multi_fasta_table.delete().where(
            self.multi_fasta_table.c.fasta_id == fasta_id
        )

        try:
            cursor = self.connection.connect()
            response = cursor.execute(query)
            cursor.commit()

            if (response.rowcount <= 0):
                multi_deleted = 900

        except Exception as e:
            multi_deleted = e

        return multi_deleted