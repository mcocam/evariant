from fastapi import APIRouter, Response, Depends, HTTPException
from models.validators.new_user import New_user
from controllers.UserController import UserController
from models.User import User

router: APIRouter = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}}
)


@router.post("/register")
async def register(new_user: New_user):
    
    response: dict[str,any] = {
        "error": True,
        "message": "904",
        "data": ""
    }
    
    userController: UserController = UserController()
    
    user_exists = await userController.check_if_user_exists(new_user.email)
    
    if user_exists:
        response["message"] = "902"
        return response
    
    try:
        user: User = User(new_user.name,
                          new_user.surname,
                          new_user.email,
                          role="client",
                          password=new_user.password)
        
        new_user_added: bool = await userController.register_user(user)
        
        if new_user_added:
            response["message"] = "900"
            response["error"] = False
        
    except Exception as e:
        print(f"Register exception: {e}")
        response["message"] = "909"
        
    return response
        
    
    
    