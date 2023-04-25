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

    async def get_single_fasta_by_id(self, id: int) -> list[str] :

        response = self.response

        try:
            query = self.fasta_table.select().where(self.fasta_table.c.id == id)
            cursor = self.connection.connect()
            rows = cursor.execute(query)

            raw_data = list[dict] = [row for row in rows]

            if raw_data:
                response["data"] = self.__parse_single_fasta(list(raw_data[0]))
                response["error"] = False
                response["message"] = "Single Fasta Found!"

            else:
                response["message"] = "Single Fasta Not Found!"
        
        except Exception as e:
            print(e)
            response["message"] = e
        
        return response
    

    # ADD SINGLE FASTA 
    def add_new_single_fasta(self,single_fasta: SingleFasta) -> bool:

        """  
        Add a new Single Fasta to database
        Enters -> Object Single Fasta
        return -> bool
        """

        new_single_fasta_added: bool = False
        query = insert(self.single_fasta_table).values(
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
                new_single_fasta_added = True

        except Exception as e:
            print(e)

        return new_single_fasta_added

    
    def __parse_single_fasta(self,raw_data: list[any] ) -> SingleFasta:

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



