
# Communication with the database
# @author: Ani Valle

from models.Fasta import Fasta
from db.get_connection import get_connection
from sqlalchemy import Engine, Table, MetaData, Column, Integer, String, DateTime, insert
from datetime import datetime

fasta_table:   Table = Table(
    "fastas",
    MetaData(),
    Column("id",Integer, primary_key=True,autoincrement='auto'),
    Column("title",String),
    Column("raw_fasta",String),
    Column("type",Integer),
    Column("creation_date",DateTime,nullable=True),
    Column("user_id",Integer)
)

class FastaDao:
    def __init__(self) -> None:
        self.connection:    Engine = get_connection()
        self.fasta_table:   Table  = fasta_table
        self.response: dict[str,any] = {"error": True, "message": "", "data": Fasta}

    async def get_fasta_by_id(self, id: int) -> list[str] :

        response = self.response

        try:
            query = self.fasta_table.select().where(self.fasta_table.c.id == id)
            cursor = self.connection.connect()
            rows = cursor.execute(query)

            raw_data = list[dict] = [row for row in rows]

            if raw_data:
                response["data"] = self.__parse_fasta(list(raw_data[0]))
                response["error"] = False
                response["message"] = "Fasta Found!"

            else:
                response["message"] = "Fasta Not Found!"
        
        except Exception as e:
            print(e)
            response["message"] = e
        
        return response
    

    # ADD FASTA 
    def add_new_fasta(self,fasta: Fasta) -> bool:
        """  Add a new Fasta to database
        Enters -> Object Fasta
        return -> bool
        """

        new_fasta_added: bool = False
        query = insert(self.fasta_table).values(
            title = fasta.title,
            raw_fasta = fasta.raw_fasta,
            type = fasta.type,
            user_id = fasta.user_id
        )

        try:
            cursor = self.connection.connect()
            response = cursor.execute(query)
            cursor.commit()
            if response.rowcount > 0:
                new_fasta_added = True

        except Exception as e:
            print(e)

        return new_fasta_added
    

    
    def __parse_fasta(self,raw_data: list[any] ) -> Fasta:

        fasta_id:       int         = raw_data[0]
        title:          str         = raw_data[1]
        raw_fasta:      str         = raw_data[2]
        type:           int         = raw_data[3]
        creation_date:  datetime    = raw_data[4]
        user_id:        int         = raw_data[5]

        fasta: Fasta = Fasta (
            title = title,
            raw_fasta = raw_fasta,
            type = type,
            user_id = user_id,
            creation_date = creation_date,
            id = user_id,)
        
        return fasta
