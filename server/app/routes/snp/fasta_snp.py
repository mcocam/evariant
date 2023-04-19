from fastapi import APIRouter, Response, Depends, HTTPException
from models.validators.new_fasta import New_fasta
from controllers.FastaController import FastaController
from models.Fasta import Fasta

router: APIRouter = APIRouter(
    prefix="/fasta",
    tags=["Fastas"],
    responses={404: {"description": "Not Found"}},
)

@router.post("/add_fasta")
async def add_fasta(new_fasta: New_fasta):

    response: dict[str,any] = {
        "error": True,
        "message": "904",
        "data": ""
    }

    fastaController: FastaController = FastaController()

    try:
        fasta: Fasta = Fasta(new_fasta.title,
                             new_fasta.raw_fasta,
                             new_fasta.type,
                             new_fasta.user_id)
        
        new_fasta_added: bool = await fastaController.register_fasta(fasta)

        if new_fasta_added:
            response["message"] = "900"
            response["error"] = False
        
    except Exception as e:
        print(f"Add Fasta Exception: {e}")
        response["message"] = "909"

    return response

