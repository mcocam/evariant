from fastapi import APIRouter, Depends, File, UploadFile
from routes.users.session import cookie, SessionData, verifier
from controllers.PhyloController import PhyloController
from controllers.FastaController import FastaController
from models.Fasta import Fasta
from controllers.MultiFastaController import MultiFastaController
from models.PhyloTree import PhyloTree

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
        "message": "925",
        "data": ""
    }
    
    phylo_controller: PhyloController = PhyloController()
    fasta_controller: FastaController = FastaController()
    multifasta_controller: MultiFastaController = MultiFastaController()
    
    try:

        ## Upload Multifasta
        content = await file.read()
        request_title = file.filename
        content = content.decode("utf-8")
       
        is_valid_fasta: int or bool = await phylo_controller.validate_multifasta(content)

        if is_valid_fasta:

            fasta: Fasta = Fasta(title=request_title,
                                 raw_fasta=content,
                                 type=0,
                                 user_id=session_data.id)

            # Fill the table with Multi FASTA
            add_multifasta_response = await fasta_controller.add_fasta(fasta)
            
            if add_multifasta_response > 0: 
                
                added_fasta_response: list[str] = await fasta_controller.get_fasta(add_multifasta_response)
                if added_fasta_response["data"]:
                    new_fasta = added_fasta_response["data"]
                    multifasta_response = await multifasta_controller.insert_fasta(new_fasta)
                    
                    if multifasta_response > 0:
                        
                        phylo: PhyloTree = phylo_controller.parse_fasta_to_phylo(new_fasta)
                        add_phylo_response: int = phylo_controller.save_phylo(phylo)
                        
                        
                        if add_phylo_response > 0:                    
                            response["error"] = False 
                            response["message"] = "900"
                            response["data"] = "Multifasta added and phylo-tree created" 
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



@router.post("/results/{fasta_id}", dependencies= [Depends(cookie)])
async def send_results_phylo(fasta_id: str, session_data: SessionData = Depends(verifier)):
    
    response: dict[str,any] = {
        "error": True,
        "message": "931",  # No results found
        "data": ""
    }

    phylo_controller: PhyloController = PhyloController()
    
    try:
        result_phyloTree = await phylo_controller.get_phylo_by_id(fasta_id)

        if result_phyloTree:
            response["error"] = False
            response["message"] = "930" # Data obtained successfully
            response["data"] = result_phyloTree
        else:
            response["message"] = "931" # No results found

    except Exception as e:
        print(f" Exception Phylo Results {e}")
        response["message"] = "932" #error exception
    
    return response