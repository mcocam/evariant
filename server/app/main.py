from fastapi import FastAPI
from routes.users.session import router as session_router
from routes.users.register import router as register_router
from routes.fasta.fasta import router as fasta_router
from routes.snp.snp import router as snp_router
from routes.phylo.phylo import router as phylo_router
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
app.include_router(session_router)
app.include_router(register_router)
app.include_router(fasta_router)
app.include_router(snp_router)
app.include_router(phylo_router)

if __name__ == "__main__":
    # To test individually
    run("main:app",host="0.0.0.0", port=5053, reload=True)

