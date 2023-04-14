from fastapi import FastAPI
from routes.users import session
from uvicorn import run

from fastapi.middleware.cors import CORSMiddleware

# Initialize fastAPI
app: FastAPI = FastAPI()

# Allowed origins
origins = [
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

# User session routes and logic
app.include_router(session.router)

if __name__ == "__main__":
    # To test individually
    run("main:app",host="0.0.0.0", port=5053, reload=True)

