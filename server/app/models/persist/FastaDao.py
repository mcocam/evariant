
# Communication with the database
# @author: Ani Valle

import datetime
from datetime import datetime
from models.Fasta import Fasta
from db.get_connection import get_connection
from sqlalchemy import Engine, Table, MetaData, Column, Integer, String, DateTime, insert, and_

fasta_table:   Table = Table(
    "fastas",
    MetaData(),
    Column("id",Integer, primary_key=True,autoincrement='auto'),
    Column("title",String),
    Column("raw_fasta",String),
    Column("type",Integer),
    Column("creation_date",DateTime, nullable=True),
    Column("user_id",Integer)
)


class FastaDao:
    def __init__(self) -> None:
        self.connection:    Engine = get_connection()
        self.fasta_table:   Table  = fasta_table
        self.response: dict[str,any] = {"error": True, "message": "", "data": Fasta}

    #----------------------------------------------------------------
    async def get_fasta_by_id(self, id: int) -> list[str] :
        """Returns a fasta identified by the given id

        Args:
            id (int): The desired fasta's id

        Returns:
            list[str]:  If found, returns the parsed fasta, a message, and a boolean indicating that there was no error.
                        If not found, simply returns a message saying so.
                        If there was an exception, returns that as the message.
        """

        response = self.response

        try:
            query = self.fasta_table.select().where(self.fasta_table.c.id == id)
            cursor = self.connection.connect()
            rows = cursor.execute(query)
            raw_data = rows.fetchone()

            if len(raw_data)>0:
                response["data"] = self.__parse_fasta(raw_data)
                response["error"] = False
                response["message"] = "Fasta Found!"

            else:
                response["message"] = "Fasta Not Found!"
        
        except Exception as e:
            print(e)
            response["message"] = e
        
        return response
    

    #----------------------------------------------------------------
    def add_new_fasta(self,fasta: Fasta) -> int:
        """  Add a new Fasta to database
        Enters -> Object Fasta
        return -> bool
        """
        """Add a new Fasta to database

        Args:
            fasta (Fasta): The new fasta to add to the database

        Returns:
            int: The id assigned to the newly added fasta
        """

        new_fasta_added: int = 0
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
                new_fasta_added = response.inserted_primary_key[0]

        except Exception as e:
            print(e)

        return new_fasta_added
    
    #----------------------------------------------------------------
    async def get_info(self, user_id: int, type_fasta) -> list[list]:
        """Get fastas table information by user id and fasta type

        Args:
            user_id (int): The owner's id
            type_fasta (bool): The type of fasta (0 = multifasta, 1 = singlefasta)

        Returns:
            list[list]: A list of all fastas belonging to the specified user.
                        Each fasta is returned as a list, separated by the columns of the database
        """

        info_fasta: list[list] = []
        
        try:
            query = self.fasta_table.select().where(
                and_(
                    self.fasta_table.c.user_id == user_id,
                    self.fasta_table.c.type == type_fasta
                ))
            cursor = self.connection.connect()
            rows = cursor.execute(query)

            info_fasta: list[list] = [row for row in rows]

        except Exception as e:
            print(f'exception dao{e}')

        return info_fasta    

    #----------------------------------------------------------------
    def __parse_fasta(self,raw_data: list[any] ) -> Fasta:
        """Reads a list of the components of a fasta, and parses it automatically into a Fasta object

        Args:
            raw_data (list[any]): A list of the fasta's components

        Returns:
            Fasta: The same information converted into a Fasta object
        """

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
            id = fasta_id,)
        
        return fasta

    #----------------------------------------------------------------
    def delete_fasta(self, fasta_id: int) -> int:
        """Removes a fasta from the database

        Args:
            fasta_id (int): The id of the fasta to delete

        Returns:
            int: A code from the list indicating if the operation was successful, or what failed exactly
        """

        fasta_deleted: int = 0

        query = self.fasta_table.delete().where(
            self.fasta_table.c.id == fasta_id
        )

        try:
            cursor = self.connection.connect()
            response = cursor.execute(query)
            cursor.commit()

            print(dir(response))

            if (response.rowcount <= 0):
                fasta_deleted = 900

        except Exception as e:
            fasta_deleted = e

        return fasta_deleted
