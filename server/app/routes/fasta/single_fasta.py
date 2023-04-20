from typing import Annotated
from fastapi import APIRouter, Response, Depends, HTTPException, File, UploadFile
from models.validators.new_fasta import New_fasta
from controllers.FastaController import FastaController
from models.Fasta import Fasta
from routes.users.session import cookie, SessionData, verifier
from uuid import uuid4 # Genera un texto random

router: APIRouter = APIRouter(
    prefix="/files",
    tags=["Fastas"],
    responses={404: {"description": "Not Found"}},
)


@router.post("/add_fasta/single", dependencies= [Depends(cookie)])
async def add_fasta(fasta_id: int, title: string, raw_fasta: string, session_data: SessionData = Depends(verifier)):
    print(f"Id del usuario: {session_data.id}")
    print(f"Id del fasta: {fasta_id}")


    # new_fasta: str = await new_file.read()
    # print(new_fasta)
    return False