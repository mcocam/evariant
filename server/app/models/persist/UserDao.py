from models.User import User
from db.get_connection import get_connection
from sqlalchemy import Engine, Table, MetaData, Column, Integer, String, DateTime, insert
from datetime import datetime
from bcrypt import hashpw
import env
import os

users_table_model: Table = Table(
    "users",
    MetaData(),
    Column("id",Integer, primary_key=True,autoincrement='auto'),
    Column("email",String,unique=True),
    Column("password", String),
    Column("name",String),
    Column("surname",String),
    Column("role",String),
    Column("creation_date",DateTime,nullable=True)
)


class UserDao:

    def __init__(self) -> None:
        
        self.connection: Engine = get_connection()
        self.user_table: Table = users_table_model
        self.response: dict[str,any] = {"error": True, "message": "", "data": User}
        self.salt: str = bytes(os.environ["PASS_SECRET"],'"utf-8')

    # ----------------------------------------------------------------
    async def get_user_by_id(self, id: int) -> list[str]:
        """Returns the information of the user with the provided id

        Args:
            id (int): The id of the desired user

        Returns:
            list[str]: A list with the user's information
        """

        response = self.response

        try:
            query = self.user_table.select().where(self.user_table.c.id == id)
            cursor = self.connection.connect()
            rows = cursor.execute(query)

            raw_data: list[dict] = [row for row in rows]

            if raw_data:

                response["data"] = self.__parse_user(list(raw_data[0]))
                response["error"] = False 
                response["message"] = "User found!"

            else:
                response["message"] = "No users found"

        except Exception as e:
            print(e)
            response["message"] = e

        return response

    # ----------------------------------------------------------------
    def check_user_credentials(self,email: str, password: str) -> bool:
        """Checks if a user has presented the correct credentials

        Args:
            email (str): User's email input
            password (str): User's password input

        Returns:
            bool: If the credentials are correct or not
        """
        
        password_utf8: str = password.encode("utf-8")
        password_hash: str = hashpw(password_utf8,self.salt)

        is_ok: bool = False

        try:
            query = self.user_table.select().where(
                    (self.user_table.c.email == email) & 
                    (self.user_table.c.password == password_hash)
                )
            
            cursor = self.connection.connect()

            rows = cursor.execute(query)

            raw_data: list[dict] = [row for row in rows]

            if raw_data:
                is_ok = True
            else:
                is_ok = False


        except Exception as e:
            print(e)

        return is_ok
    
    # ----------------------------------------------------------------
    def get_user_by_email(self, email: str) -> list[dict]:
        """Returns the information of the user with the provided email

        Args:
            email (str): The email of the desired user

        Returns:
            list[str]: A list with the user's information
        """
        
        user: list[dict] = []
        
        try:
            
            query = self.user_table.select().where(
                (self.user_table.c.email == email)
            )
            
            cursor = self.connection.connect()
            
            rows = cursor.execute(query)
            
            user: list[dict] = [row for row in rows]
            
        except Exception as e:
            print(e)
        
        return user
    
    # ----------------------------------------------------------------
    def add_new_user(self,user: User) -> bool:
        """Adds a new user to the database

        Args:
            user (User): A User object

        Returns:
            bool: Whether the operation was successful or not
        """
        
        new_user_added: bool = False
        query = insert(self.user_table).values(
            email=user.email,
            password= hashpw(user.passowrd.encode('utf-8'),self.salt),
            name=user.name,
            surname=user.surname,
            role=user.role
        )
        
        try:
            cursor = self.connection.connect()
            response = cursor.execute(query)
            cursor.commit()
            if response.rowcount > 0:
                new_user_added = True
                
            
        except Exception as e:
            print(e)
        
        return new_user_added


    # ----------------------------------------------------------------
    def __parse_user(self, raw_data: list[any]) -> User:
        """Reads a list of the information of a user, and parses it automatically into a User object

        Args:
            raw_data (list[any]): A list of the user's information

        Returns:
            User: The same information converted into a User object
        """

        user_id:        int         = raw_data[0]
        email:          str         = raw_data[1]
        password:       str         = raw_data[2]
        name:           str         = raw_data[3]
        surname:        str         = raw_data[4]
        role:           str         = raw_data[5]
        creation_date:  datetime    = raw_data[6]

        user: User = User(
            name = name,
            surname = surname,
            email = email,
            role = role,
            password = password,
            id = user_id,
            creation_date = creation_date)

        return user
