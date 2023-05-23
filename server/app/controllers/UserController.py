
from models.persist.UserDao import UserDao
from models.User import User


class UserController:

    def __init__(self) -> None:
        self.dao = UserDao()


    async def do_login(self, email: str, password: str) -> bool:
        """Checks if the login info is correct

        Args:
            email (str): Email input by user
            password (str): Password input by user

        Returns:
            bool: Returns true if email and password matches with the ones saved in the database
        """

        result: bool = False

        try:
            result = self.dao.check_user_credentials(email,password)

        except Exception as e:
            print(e)

        return result
    
    async def check_if_user_exists(self, email: str) -> bool:
        """Checks if an email is already associated with a user

        Args:
            email (str): The email to check

        Returns:
            bool: False if user doesn't exist, True if it does
        """
        
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
        """Gets a user's info

        Args:
            email (_type_): The email of the desired user

        Returns:
            list: A list of the user's info
        """
        
        data = {}
        
        try:
            result = self.dao.get_user_by_email(email)
            data = list(result[0])
            
        except Exception as e:
            print(f"Get user infor error: {e}")
            
        return data
        
        
    
    async def register_user(self, new_user: User) -> bool:
        """Adds a new user to the database

        Args:
            new_user (User): A User object to be stored in the db

        Returns:
            bool: Indicates if it's been successfully added
        """
        
        new_user_added: bool = False
        
        try:
            new_user_added = self.dao.add_new_user(new_user)
        except Exception as e:
            print(e)
        
        return new_user_added
