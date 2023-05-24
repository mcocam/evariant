"""
SNP Results Router
Author: Melania Prado

This module defines the API router for retrieving SNP results based on a given FASTA ID.
"""


from fastapi import APIRouter, Depends, HTTPException
from controllers.SnpController import SnpController
from controllers.FastaController import FastaController
from routes.users.session import cookie, SessionData, verifier
from models.utils.scraper_utils import get_snpedia_pages, get_snp_genotypes, get_snp_articles, get_articles_urls, get_snp_articles_titles, get_regions_values, get_regions_desc


router: APIRouter = APIRouter(
    prefix="/snp",
    tags=["SNPFinder"],
    responses={404: {"description": "Not found"}}
)


@router.get("/results/{fasta_id}", dependencies= [Depends(cookie)])
async def get_snp_results(fasta_id: str, session_data: SessionData = Depends(verifier)):
    """
    Retrieve the SNPs for a given FASTA ID.

    Args:
        fasta_id (str): The FASTA ID as a string.
        session_data (SessionData): An object representing the current user session data.

    Returns:
        dict: A dictionary containing the SNPs for the given FASTA ID and their related data from SNPedia.
        
    Raises:
        HTTPException: If the user does not have access to the request.
        HTTPException: If an error occurs during the retrieval process.
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

        snpedia_pages = get_snpedia_pages(snp_refs)
        snp_genotypes = get_snp_genotypes(snp_refs, snpedia_pages)
        snp_articles = get_snp_articles(snp_refs, snpedia_pages)
        snp_articles_titles = get_snp_articles_titles(snp_refs, snpedia_pages)
        snp_articles_url = get_articles_urls(snp_refs, snpedia_pages)
        snp_regions_values = get_regions_values(snp_refs, snpedia_pages)
        snp_regions_desc = get_regions_desc(snp_refs, snpedia_pages)

        # Place all the data in a dictionary
        snp_data_dict = {
            'snp_ref_nucleotides': snp_ref_nucleotides,
            'snp_var_nucleotides': snp_var_nucleotides,
            'snp_refs': snp_refs,
            'snp_genotypes': snp_genotypes,
            'snp_articles': snp_articles,
            'snp_articles_titles': snp_articles_titles,
            'snp_articles_url': snp_articles_url,
            'snp_regions_values': snp_regions_values,
            'snp_regions_desc': snp_regions_desc
        }
        print('snp_data_dict')

        return snp_data_dict

    except HTTPException:
        print(HTTPException)
        raise
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    