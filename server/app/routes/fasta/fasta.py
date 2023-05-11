from fastapi import APIRouter, Depends, File, UploadFile

from controllers.FastaController import FastaController
from controllers.SingleFastaController import SingleFastaController
from controllers.MultiFastaController import MultiFastaController
from controllers.SnpController import SnpController
from controllers.PhyloController import PhyloController

from models.Fasta import Fasta
from models.SingleFasta import SingleFasta
from models.MultiFasta import MultiFasta
from models.Snp import Snp
from models.PhyloTree import PhyloTree

from models.utils.SnpHandler import SnpHandler

from routes.users.session import cookie, SessionData, verifier


router: APIRouter = APIRouter(
    prefix="/files",
    tags=["Fastas"],
    responses={404: {"description": "Not Found"}},
)


@router.post("/add_fasta", dependencies= [Depends(cookie)])
async def get_file(file: UploadFile = File(...), session_data: SessionData = Depends(verifier)):
    
    response: dict = {
        "error": True,
        "message": "",
        "data": ""
    }
    
    fasta_controller: FastaController = FastaController()
    single_fasta_controller: SingleFastaController = SingleFastaController()
    snp_controller: SnpController = SnpController()
    snp_handler: SnpHandler = SnpHandler()
    
    
    try:
        
        ## Upload Fasta
        content = await file.read()
        requests_title = file.filename
        content = content.decode("utf-8")
        
        fasta_type: int = await fasta_controller.get_type_fasta(content)
        
        if fasta_type == 1:
            
            is_valid_fasta = await fasta_controller.is_valid_fasta(content)
            
            if is_valid_fasta[0]:
                assembly: str = is_valid_fasta[1]
                chromosome: str = is_valid_fasta[2]
                strand: int = is_valid_fasta[3]
                position: str = is_valid_fasta[4]
                position_split: list[int] = [int(position) for position in position.split(":")]
                sequence: str = is_valid_fasta[5]
                
                fasta: Fasta = Fasta(title=requests_title,
                                     raw_fasta=content,
                                     type=1,
                                     user_id=session_data.id)
            
            # Fill Single Fasta Table
                
                add_fasta_response = await fasta_controller.add_fasta(fasta)
                if add_fasta_response > 0:
                    uploaded_fasta_response: dict = await fasta_controller.get_fasta(add_fasta_response)
                    uploaded_fasta: Fasta = uploaded_fasta_response["data"]
                    
                    single_fasta_inserted_id = single_fasta_controller.parse_single_fasta(uploaded_fasta)
                    
                    if single_fasta_inserted_id > 0:
                        
                        single_fasta_inserted: SingleFasta = await single_fasta_controller.get_single_fasta_by_id(single_fasta_inserted_id)
                        ref_genome_seq: str = snp_handler.get_reference_sequence(single_fasta_inserted)
                        differences: list = snp_handler.identify_differences(ref_genome_seq,single_fasta_inserted)
                        snps: list[Snp] = snp_handler.get_snp_by_positions(differences,single_fasta_inserted)
                        
                        detected_snps: int = 0
                        for snp in snps:
                            inserted: int = await snp_controller.save_snps_to_db(snp)
                            detected_snps += inserted
                            
                            
                        response["error"] = False 
                        response["message"] = "912"
                        response["data"] = f"Number of SNPs detected: {detected_snps}"
                        
            else:
                response["message"] = "911"
        elif fasta_type == 0:
            response["message"] = "911"
        
        
    except Exception as e:
        print(f"Add fasta error: {e}")
        response["message"] = "913" # Add fasta error
    #print(content)
    
    return response



@router.get("/requests", dependencies= [Depends(cookie)])
async def requests_snp(session_data: SessionData = Depends(verifier)):

    response: dict[str,any] = {
        "error": True,
        "message": "914",  # No results found
        "data": ""
    }

    try:
        fasta_Controller: FastaController = FastaController()

        # Logged in User ID
        user_id = session_data.id
        # fasta id of the app "SNP Finder"
        single_fasta: int = 1

        # Get data
        data = await fasta_Controller.get_fasta_info(user_id, single_fasta)
        # print(f"llega al fasta {data}")

        if data:
            response["error"] = False
            response["message"] = "915" # Data obtained successfully
            response["data"] = data
        else:
            response["message"] = "914" # No results found


    except Exception as e:
        print(e)
        response["message"] = "916" #error exception

    return response

@router.get("/delete_fasta/{id}", dependencies= [Depends(cookie)])
async def delete_fasta(id: int, session_data: SessionData = Depends(verifier)):

    response: dict[str,any] = {
        "error": True,
        "message": "914",  # No results found
        "data": ""
    }

    try:
        fasta_controller: FastaController = FastaController()
        sinle_controller: SingleFastaController = SingleFastaController()
        multi_controller: MultiFastaController = MultiFastaController()
        snp_controller: SnpController = SnpController()
        phylo_controller: PhyloController = PhyloController()

        # Logged in User ID
        user_id = session_data.id

        # Get data
        data = await snp_controller.del_snp(id)
        data = await phylo_controller.del_phylo(id)
        data = await sinle_controller.del_single(id)
        data = await multi_controller.del_multi(id)
        data = await fasta_controller.del_fasta(id)
        # print(f"llega al fasta {data}")

        if data:
            response["error"] = False
            response["message"] = "917" # Data deleted successfully
            response["data"] = data
        else:
            response["message"] = "914" # No results found


    except Exception as e:
        print(e)
        response["message"] = "916" #error exception

    return response