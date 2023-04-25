from requests import get, Response
from models.SingleFasta import SingleFasta

class SnpHandler:
    
    def __init__(self) -> None:
        self.ucsc_base_endpoint: str = "https://api.genome.ucsc.edu"
        
        
    def check_if_assembly_exists(self, assembly: str) -> bool:
        """Checks if submitted genome reference exists.
            Please, keep in main that the assembly name is checked as it comes
            and is case sensitive

        Args:
            assembly (str): assembly name as listed on UCSC

        Returns:
            bool: true if genome name exists; false otherwise
        """

        assembly_ok: bool = False
        endpoint: str = f"{self.ucsc_base_endpoint}/list/ucscGenomes"
        
        try:
            response: Response = get(endpoint)
            available_genomes: dict = response.json()["ucscGenomes"]
            available_genomes_list: list[str] = list(available_genomes.keys())
            
            if assembly in available_genomes_list:
                assembly_ok = True
            
            
        except Exception as e:
            print(f"check if genome exists error: {e}")
        
        return assembly_ok
    
    
    def get_reference_sequence(self, single_fasta: SingleFasta) -> str:
        
        ref_seq: str = ""
        
        endpoint: str = f"{self.ucsc_base_endpoint}/getData/sequence"
        
        params = {
            'genome': single_fasta.getAssembly(),
            'chrom': single_fasta.getChromosome(),
            'start': single_fasta.getStartLoc(),
            'end': single_fasta.getEndLoc()
        }
        
        try:
            response: Response = get(endpoint,params)
            ref_seq = response.json()["dna"]
        except Exception as e:
            print(f"SnpHandler, get_reference_seq error: {e}")
        
        return ref_seq
    
    def identify_differences():
        pass







if __name__ == "__main__":
    
    single_fasta_test: SingleFasta = SingleFasta(
        1, 
        'CTCGGGCACAGCATTCATGGAAAGGAAAGGTGTACGGGACATGCCCGAGGATCCTCAGTCCCACAGAAACAGGGAGGGGCTGGGAAGCTCATTCTACAGATGGGG',
        'hg38', 
        'chr3',
        1 , 
        8762634, 
        8762739
    )
    
    snp_handler: SnpHandler = SnpHandler()
    #assembly_exists: bool = snp_handler.check_if_assembly_exists("hg38")
    ref_seq: str = snp_handler.get_reference_sequence(single_fasta=single_fasta_test)
    
    print(ref_seq)
    
    