from fastapi import APIRouter, Response, Depends, HTTPException
from models.validators.credentials import Credentials
from controllers.UserController import UserController
from pydantic import BaseModel
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi_sessions.session_verifier import SessionVerifier
from fastapi_sessions.backends.implementations import InMemoryBackend
from uuid import UUID, uuid4
import env
import os

class SessionData(BaseModel):
    email: str
    name: str
    surname: str
    id: int

cookie_params = CookieParameters()
backend = InMemoryBackend[UUID, SessionData]()

# Uses UUID
cookie = SessionCookie(
    cookie_name="evariantSession",
    identifier="general_verifier",
    auto_error=True,
    secret_key=os.environ["SESSION_SECRERT"],
    cookie_params=cookie_params
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}}
)


# Session verifier
class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(
        self,
        *,
        identifier: str,
        auto_error: bool,
        backend: InMemoryBackend[UUID, SessionData],
        auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """If the session exists, it is valid"""
        return True


verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=backend,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)



@router.post("/login")
async def login(credentials: Credentials, res: Response):

    response: dict[str,any] = {
        "error": True,
        "message": "904",
        "data": ""
    }

    try:

        userController: UserController = UserController()

        email: str = credentials.email
        password: str = credentials.password

        user_exists: bool = await userController.do_login(email,password)

        if user_exists:

            session = uuid4()
            user_info = await userController.get_user_info(email)
            data = SessionData(
                email = user_info[1],
                name = user_info[3],
                surname = user_info[4],
                id = user_info[0]
                )

            await backend.create(session, data)
            cookie.attach_to_response(res, session)

            response["error"] = False
            response["message"] = "900"
        else:
            response["message"] = "904"
 
    except Exception as e:
        print(f"Exception from login route: {e}")
        response["message"] = "909"

    return response

@router.post("/verify", dependencies=[Depends(cookie)])
async def verify():
    return HTTPException(status_code=200, detail="Session is correct")

@router.post("/logout")
async def del_session(response: Response, session_id: UUID = Depends(cookie)):
    
    # await backend.delete(session_id)
    # cookie.delete_from_response(response)
    # return "deleted session"
    res: dict[str,any] = {
        "error": True,
        "message": "904",
        "data": ""
    }
    
    try:
        await backend.delete(session_id)
        cookie.delete_from_response(response)
        res["error"] = False 
        res["message"] = "900"
    except Exception as e:
        print(f"Error on delete session: {e}")
        res["message"] = "909"
        
    return res


