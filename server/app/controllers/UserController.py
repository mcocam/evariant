
from models.persist.UserDao import UserDao
from pydantic import BaseModel
from models.User import User
import env
import os

class UserController:

    def __init__(self) -> None:
        self.dao = UserDao()


    async def do_login(self, email: str, password: str) -> bool:

        result: bool = False

        try:
            result = self.dao.check_user_credentials(email,password)

        except Exception as e:
            print(e)

        return result
    
    async def check_if_user_exists(self, email: str) -> bool:
        
        user_exists: bool = True 
        
        try:
            result = self.dao.get_user_by_email(email)
            
            if len(result) == 0:
                user_exists = False
            
        except Exception as e:
            print(e)
            pass
        
        return user_exists
    
    async def get_user_info(self, email):
        
        data = {}
        
        try:
            result = self.dao.get_user_by_email(email)
            data = list(result[0])
            
        except Exception as e:
            print(f"Get user infor error: {e}")
            
        return data
        
        
    
    async def register_user(self, new_user: User) -> bool:
        
        new_user_added: bool = False
        
        try:
            new_user_added = self.dao.add_new_user(new_user)
        except Exception as e:
            print(e)
        
        return new_user_added
