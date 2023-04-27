from typing import Annotated
from fastapi import APIRouter, Response, Depends, File, UploadFile
from uvicorn import run
from fastapi.middleware.cors import CORSMiddleware

from controllers.FastaController import FastaController
from controllers.SingleFastaController import SingleFastaController
from controllers.SnpController import SnpController

from models.Fasta import Fasta
from models.SingleFasta import SingleFasta
from models.Snp import Snp

from models.utils.SnpHandler import SnpHandler

from routes.users.session import cookie, SessionData, verifier
from uuid import uuid4 # Genera un texto random


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
                
                fasta: Fasta = Fasta(title=uuid4(),
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
                        response["message"] = f"Number of SNPs detected: {detected_snps}"
                        response["data"] = ""
                        
            else:
                response["message"] = "915"
            
            pass
        elif fasta_type == 0:
            pass
        
        
    except Exception as e:
        print(f"Add fasta error: {e}")
    
    
    
    #print(content)
    
    return response





























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

