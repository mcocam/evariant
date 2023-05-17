# Communication with the database
# @author: Marc Garcia

from models.SingleFasta import SingleFasta
from db.get_connection import get_connection
from sqlalchemy import Engine, Table, MetaData, Column, Integer, String, DateTime, insert
from datetime import datetime

single_fasta_table:   Table = Table(
    "single_fastas",
    MetaData(),
    Column("fasta_id",Integer, primary_key=True),
    Column("sequence",String),
    Column("assembly",String),
    Column("chromosome",String),
    Column("strand",Integer),
    Column("start_loc",Integer),
    Column("end_loc",Integer)
)

class SingleFastaDao:
    def __init__(self) -> None:
        self.connection:    Engine = get_connection()
        self.single_fasta_table:   Table  = single_fasta_table
        self.response: dict[str,any] = {"error": True, "message": "", "data": SingleFasta}

    #----------------------------------------------------------------
    async def get_single_fasta_by_id(self, id: int) -> SingleFasta :
        """Returns the SingleFasta identified by the given id

        Args:
            id (int): The id number of the desired fasta

        Returns:
            SingleFasta: A SingleFasta object
        """

        response = self.response

        try:
            query = self.single_fasta_table.select().where(self.single_fasta_table.c.fasta_id == id)
            cursor = self.connection.connect()
            rows = cursor.execute(query)
            raw_data = rows.fetchone()

            if raw_data:
                response["data"] = self.__parse_single_fasta(raw_data)
                response["error"] = False
                response["message"] = "Single Fasta Found!"

            else:
                response["message"] = "Single Fasta Not Found!"
        
        except Exception as e:
            print(e)
            response["message"] = e
        
        return response
    

    #----------------------------------------------------------------
    def add_new_single_fasta(self,single_fasta: SingleFasta) -> bool:
        """Add a new Single Fasta to database

        Args:
            single_fasta (SingleFasta): A SingleFasta object

        Returns:
            bool: Indicates if the operation was successful
        """      

        inserted_response: int = 0

        query = insert(self.single_fasta_table).values(
            fasta_id = single_fasta.fasta_id,
            sequence = single_fasta.sequence,
            assembly = single_fasta.assembly,
            chromosome = single_fasta.chromosome,
            strand = single_fasta.strand,
            start_loc = single_fasta.start_loc,
            end_loc = single_fasta.end_loc
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
    def __parse_single_fasta(self,raw_data: list[any] ) -> SingleFasta:
        """Takes a list of the fasta's sections and parses them into a SingleFasta object

        Args:
            raw_data (list[any]): A list with all sections

        Returns:
            SingleFasta: A SingleFasta object
        """

        fasta_id:       int         = raw_data[0]
        sequence:       str         = raw_data[1]
        assembly:       str         = raw_data[2]
        chromosome:     str         = raw_data[3]
        strand:         int         = raw_data[4]
        start_loc:      int         = raw_data[5]
        end_loc:        int         = raw_data[6]

        fasta: SingleFasta = SingleFasta (
            fasta_id = fasta_id,
            sequence = sequence,
            assembly = assembly,
            chromosome = chromosome,
            strand = strand,
            start_loc = start_loc,
            end_loc = end_loc)
        
        return fasta
    
    #----------------------------------------------------------------
    def delete_single(self, fasta_id: int) -> int:
        """Removes a single fasta from the database

        Args:
            fasta_id (int): The id of the fasta to delete

        Returns:
            int: A code from the list indicating if the operation was successful, or what failed exactly
        """

        single_deleted: int = 0

        query = self.single_fasta_table.delete().where(
            self.single_fasta_table.c.fasta_id == fasta_id
        )

        try:
            cursor = self.connection.connect()
            response = cursor.execute(query)
            cursor.commit()

            print(dir(response))

            if (response.rowcount <= 0):
                single_deleted = 900

        except Exception as e:
            single_deleted = e

        return single_deleted


