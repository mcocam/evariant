
from models.persist.UserDao import UserDao
from pydantic import BaseModel

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
