from fastapi import APIRouter, Response, Depends, HTTPException, File, UploadFile
from routes.users.session import cookie, SessionData, verifier
from models.persist.PhyloDao import PhyloDao
from controllers.PhyloController import PhyloController
from controllers.FastaController import FastaController
from models.Fasta import Fasta

router: APIRouter = APIRouter(
    prefix="/phylo",
    tags=["Phylogenetic Trees"],
    responses={404: {"description": "Not found"}}
)

@router.post("/add_multi_fasta",dependencies= [Depends(cookie)])
async def get_phylos(file: UploadFile = File(...), session_data: SessionData = Depends(verifier)):

    # prova = phylo_dao.get_phylo_by_fasta_id(4)
    #prova = phylo_dao.get_phylos_by_user_id(1)

    response: dict = {
        "error": True,
        "message": "",
        "data": ""
    }
    
    phylo_controller: PhyloController = PhyloController()
    fasta_controller: FastaController = FastaController()
    
    try:

        ## Upload Multifasta
        content = await file.read()
        request_title = file.filename
        content = content.decode("utf-8")
       
        fasta_type: int or bool = await phylo_controller.validate_multifasta(content)

        if fasta_type == 0:

            fasta: Fasta = Fasta(title=request_title,
                                 raw_fasta=content,
                                 type=0,
                                 user_id=session_data.id)

            # Fill the table with Multi FASTA
            add_multifasta_response = await fasta_controller.add_fasta(fasta)

            response["error"] = False 
            response["message"] = "926"
            response["data"] = f"Add Multifasta Response  {add_multifasta_response }" 
        else:
            response["message"] = "925" # Multi fasta incorrect

    except Exception as e:
        print(f"Add Multi fasta error: {e}")
        response["message"] = "927" # Add fasta error
    #print(content)
    
    return response
    

@router.get("/requests", dependencies= [Depends(cookie)])
async def requests_phylo(session_data: SessionData = Depends(verifier)):

    response: dict[str,any] = {
        "error": True,
        "message": "921",  # No results found
        "data": ""
    }

    try:

        fasta_Controller: FastaController = FastaController()

        # Logged in User ID
        user_id = session_data.id
        # fasta id of the app "Phylo Trees"
        multi_fasta: int = 0

        # Get data
        data = await fasta_Controller.get_fasta_info(user_id, multi_fasta)
        # print(f"llega al phylo {data}")

        if data:
            response["error"] = False
            response["message"] = "920" # Data obtained successfully
            response["data"] = data
        else:
            response["message"] = "921" # No results found

    except Exception as e:
        print(e)
        response["message"] = "922" #error exception

    return response

    pass