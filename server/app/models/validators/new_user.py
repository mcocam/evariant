from pydantic import BaseModel, validator
import re

class New_user(BaseModel):
    
    email: str
    password: str
    name: str
    surname: str 


    @validator('email')
    def email_validator(cls, email):
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        
        if re.fullmatch(regex,email):
            return email 
        else:
            raise ValueError("Invalid email data")
        
    @validator('password')
    def password_validator(cls, password):

        regex = re.compile(r'(?=.*[a-zA-Z])(?=.*[0-9])')

        if len(password) < 5 and len(password) > 20:
            raise ValueError("Password too short")
        
        if re.search(regex,password) is None:
            raise ValueError("Password does not fulfill requirements")
        
        return password
    
    @validator('name')
    def name_validator(cls, name):

        regex = re.compile(r"^[A-Za-z\s.'-]*[A-Za-z][A-Za-z\s.'-]*$")

        if len(name) == 0 or name == None:
            raise ValueError("No valid name provided")
        
        if re.search(regex,name) is None:
            raise ValueError("Names cannot contain numbers")
        
        return name
    
    @validator('surname')
    def surname_validator(cls, surname):

        regex = re.compile(r"^[A-Za-z\s.'-]*[A-Za-z][A-Za-z\s.'-]*$")

        if len(surname) == 0 or surname == None:
            raise ValueError("No valid name provided")
        
        if re.search(regex,surname) is None:
            raise ValueError("Names cannot contain numbers")
        
        return surname