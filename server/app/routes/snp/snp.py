# SNP results router
# @author: Melania Prado

from fastapi import APIRouter, Depends, HTTPException
from controllers.SnpController import SnpController
from controllers.FastaController import FastaController
from routes.users.session import cookie, SessionData, verifier
from models.utils.scraper_utils import get_snpedia_pages, get_snp_genotypes, get_snp_articles, get_articles_urls, get_snp_articles_titles


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
        A dictionary with the SNPs for the given FASTA ID and their related data from SNPedia.
    """

    try:
        snp_controller = SnpController()

        # Get the request associated with the fasta_id
        fasta_controller = FastaController()
        request = await fasta_controller.get_fasta(fasta_id)
        request = request['data']
        fasta_user_id = request.get_user_id()
        print(fasta_user_id)

        # Verify if the user has access to the request
        if session_data.id != fasta_user_id:
            raise HTTPException(status_code=403, detail="User does not have access to the request.")
        
        snps = await snp_controller.get_snps_by_fasta_id(fasta_id)
        snp_ref_nucleotides = [snp.get_ref_nucleotide() for snp in snps]
      
        snp_var_nucleotides = [snp.get_var_nucleotide() for snp in snps]
     
        snp_refs = await snp_controller.get_snp_refs_by_fasta_id(fasta_id)
        print('snp_refs')
        print(snp_refs)
        #snp_refs = ['rs1815739', 'rs6152', 'rs1800497'] # For testing purposes
        snpedia_pages = get_snpedia_pages(snp_refs)
        snp_genotypes = get_snp_genotypes(snp_refs, snpedia_pages)
        snp_articles = get_snp_articles(snp_refs, snpedia_pages)
        snp_articles_titles = get_snp_articles_titles(snp_refs, snpedia_pages)
        snp_articles_url = get_articles_urls(snp_refs, snpedia_pages)


        print('snp_ref_nucleotides')
        print(snp_ref_nucleotides)

        #return snp_genotypes, snp_articles, snp_articles_titles, snp_articles_url
        #snp_data = get_snp_data(snp_refs, snpedia_pages)

        # Recopilar los resultados en un diccionario
        snp_data_dict = {
            'snp_ref_nucleotides': snp_ref_nucleotides,
            'snp_var_nucleotides': snp_var_nucleotides,
            'snp_refs': snp_refs,
            'snp_genotypes': snp_genotypes,
            'snp_articles': snp_articles,
            'snp_articles_titles': snp_articles_titles,
            'snp_articles_url': snp_articles_url
        }
        print('snp_data_dict')
        print(snp_data_dict)
        return snp_data_dict

    except HTTPException:
        print(HTTPException)
        raise
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    