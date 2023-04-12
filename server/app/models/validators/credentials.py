from pydantic import BaseModel, validator 
import re



class Credentials(BaseModel):

    email: str | None
    password: str | None


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

        if len(password) < 5:
            raise ValueError("Password too short")
        
        if re.search(regex,password) is None:
            raise ValueError("Password does not fulfill requirements")
        
        return password