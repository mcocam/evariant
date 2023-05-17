# Class Snp
# @author: Melania Prado

from fastapi import APIRouter, Depends, HTTPException
from controllers.SnpController import SnpController
from controllers.FastaController import FastaController
from routes.users.session import cookie, SessionData, verifier

router: APIRouter = APIRouter(
    prefix="/snp",
    tags=["SNPFinder"],
    responses={404: {"description": "Not found"}}
)


@router.get("/results/{fasta_id}", dependencies= [Depends(cookie)])
async def get_snp_results(fasta_id: str, session_data: SessionData = Depends(verifier)):
    """
    Returns the SNPs for a given fasta_id.

    Args:
        fasta_id: A string with the FASTA ID.
        session: A SessionData object with the current user session data.

    Returns:
        A list with the SNPs for the given FASTA ID.
    """

    try:
        snp_controller = SnpController()

        # Get the request associated with the fasta_id
        fasta_controller = FastaController()
        request = await fasta_controller.get_fasta(fasta_id)
        request = request['data']
        fasta_user_id = request.get_user_id()
        print(fasta_user_id)
        # Verify if the user has access to the 
        if session_data.id != fasta_user_id:
        #if session_data.id != request["user_id"]:
            raise HTTPException(status_code=403, detail="User does not have access to the request.")

        snps = await snp_controller.get_snps_by_fasta_id(fasta_id)
        
        return snps
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
