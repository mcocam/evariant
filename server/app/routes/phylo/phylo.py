from fastapi import APIRouter, Response, Depends, HTTPException
from routes.users.session import cookie, SessionData, verifier
from models.persist.PhyloDao import PhyloDao

router: APIRouter = APIRouter(
    prefix="/phylo",
    tags=["Phylogenetic Trees"],
    responses={404: {"description": "Not found"}}
)

@router.get("/test",dependencies= [Depends(cookie)])
async def get_phylos():
    
    phylo_dao: PhyloDao = PhyloDao()
    
    prova = phylo_dao.get_phylo_by_fasta_id(4)
    
    print(prova)
    
    
    pass