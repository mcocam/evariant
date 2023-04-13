from fastapi import FastAPI
from server.app.routes.session import session
from uvicorn import run
from models.persist.UserDao import UserDao

from fastapi.middleware.cors import CORSMiddleware




app: FastAPI = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(session.router)

@app.get("/")
async def login_trial():
    
    
    
    return ""



if __name__ == "__main__":
    # To test individually
    run("main:app",host="0.0.0.0", port=5053, reload=True)

