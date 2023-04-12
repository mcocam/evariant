from models.User import User
from db.get_connection import get_connection
from sqlalchemy import Engine, Table, MetaData, Column, Integer, String, DateTime
from datetime import datetime

users_table_model: Table = Table(
    "users",
    MetaData(),
    Column("id",Integer, primary_key=True),
    Column("email",String,unique=True),
    Column("password", String),
    Column("name",String),
    Column("surname",String),
    Column("role",String),
    Column("creation_date",DateTime)
)


class UserDao:

    def __init__(self) -> None:
        
        self.connection: Engine = get_connection()
        self.user_table: Table = users_table_model
        self.response: dict[str,any] = {"error": True, "message": "", "data": User}

    async def get_user_by_id(self, id: int) -> list[str]:

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


    def check_user_credentials(self,email: str, password: str) -> dict[str,any]:

        is_ok: bool = False

        try:
            query = self.user_table.select().where(
                    (self.user_table.c.email == email) & 
                    (self.user_table.c.password == password)
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


    def __parse_user(self, raw_data: list[any]) -> User:

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
