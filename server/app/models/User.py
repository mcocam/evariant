# Class User
# @author: Marc Coca

from datetime import datetime

class User:

    def __init__(self,
                 name: str,
                 surname: str,
                 email: str,
                 role: str,
                 password: str = None,
                 id: int = None,
                 creation_date: datetime = None
                 ) -> None:
        
        self.name: str = name
        self.surname: str = surname
        self.email: str = email
        self.role: str = role 
        self.passowrd: str = password
        self.id: int = id
        self.creation_date: datetime = creation_date

    # GETTERS
    def get_name(self) -> str:
        return self.name
    
    def get_surname(self) -> str:
        return self.surname
    
    def get_email(self) -> str:
        return self.email
    
    def get_role(self) -> str:
        return self.role
    
    def get_password(self) -> str:
        return self.password
    
    def get_id(self) -> int:
        return self.id
    
    def get_creation_date(self) -> datetime:
        return self.get_creation_date
    
    # SETTERS
    def set_name(self, name: str) -> None:
        self.name = name

    def set_surname(self, surname: str) -> None:
        self.surname = surname 

    def set_email(self, email: str) -> None:
        self.email = email 

    def set_role(self, role: str) -> None:
        self.role = role 

    def set_password(self, password: str) -> None:
        self.password = password

    def set_id(self, id: int) -> None:
        self.id = id
