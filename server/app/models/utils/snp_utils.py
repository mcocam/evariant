from Bio import Entrez 
from models.SingleFasta import SingleFasta

def get_reference_genome(genome_assembly: str, 
                         chromosome: str,
                         strand: int, 
                         start: int,
                         end: int) -> str:
    pass