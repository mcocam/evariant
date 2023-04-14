from pydantic import BaseModel, validator


class New_user(BaseModel):
    
    email: str
    password: str
    name: str
    surname: str 
