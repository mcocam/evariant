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


@router.post("/add_fasta", dependencies= [Depends(cookie)])
async def add_fasta(new_file: UploadFile = File(...), session_data: SessionData = Depends(verifier)):
    print("Id del usuario"+session_data.id)
    new_fasta: str = await new_file.read()
    #print(new_fasta)
    return False



























    # response: dict[str,any] = {
    #     "error": True,
    #     "message": "904",
    #     "data": ""
    # }

    # fastaController: FastaController = FastaController()
# response: dict[str,any] = {
    #     "error": True,
    #     "message": "904",
    #     "data": ""
    # }

    # fastaController: FastaController = FastaController()

    # try:
    #     fasta: Fasta = Fasta(new_file.title,
    #                          new_file.raw_fasta,
    #                          new_file.type,
    #                          new_file.user_id)
        
    #     new_file_added: bool = await fastaController.register_fasta(fasta)

    #     if new_file_added:
    #         response["message"] = "900"
    #         response["error"] = False
        
    # except Exception as e:
    #     print(f"Add Fasta Exception: {e}")
    #     response["message"] = "909"

    # return response


    # try:
    #     fasta: Fasta = Fasta(new_file.title,
    #                          new_file.raw_fasta,
    #                          new_file.type,
    #                          new_file.user_id)
        
    #     new_file_added: bool = await fastaController.register_fasta(fasta)

    #     if new_file_added:
    #         response["message"] = "900"
    #         response["error"] = False
        
    # except Exception as e:
    #     print(f"Add Fasta Exception: {e}")
    #     response["message"] = "909"

    # return response

