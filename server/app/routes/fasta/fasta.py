from typing import Annotated
from fastapi import APIRouter, Response, Depends, File, UploadFile
from uvicorn import run
from fastapi.middleware.cors import CORSMiddleware

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
async def get_file(file: UploadFile = File(...), session_data: SessionData = Depends(verifier)):
    content = await file.read()
    print(content)

    # 




    return {"data": "Content uploaded successfully"}

if __name__ == "__main__":
    run("main:app",host="0.0.0.0",port=5050, reload=True)




# async def add_fasta(new_file: UploadFile  = File(...), session_data: SessionData = Depends(verifier)):
#     print(f"Id del usuario: {session_data.id}")
    
#     new_fasta: str = await new_file.read()
#     print(new_fasta)
    
#     response = f"archivo recibido {new_fasta}"
#     return response






























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

