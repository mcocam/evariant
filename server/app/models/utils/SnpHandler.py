from requests import get, Response
# from SingleFasta import SingleFasta
# from Snp import Snp

from models.SingleFasta import SingleFasta 
from models.Snp import Snp
from Bio import Entrez
import re


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
            'start': single_fasta.getStartLoc() - 1,
            'end': single_fasta.getEndLoc()
        }
        
        try:
            response: Response = get(endpoint,params)
            ref_seq = response.json()["dna"]
            
            if len(ref_seq) > 0:
                ref_seq = ref_seq.upper()
            
        except Exception as e:
            print(f"SnpHandler, get_reference_seq error: {e}")
        

        return ref_seq
    
    def identify_differences(self, ref_seq:str, single_fasta: SingleFasta) -> list[dict]:
        
        differences: list[int] = []
        difference: dict = {
            "position": None,
            "reference_nucleotide": None,
            "variant_nucleotide": None,
            "chromosome": None
        }
        
        start_position: int = single_fasta.getStartLoc()
        user_seq: str = single_fasta.getSequence()
        
        for i, nucleotide in enumerate(ref_seq):
            
            if nucleotide != user_seq[i]:
                position = start_position + i
                reference_nucleotide = nucleotide
                variant_nucleotide = user_seq[i]
                
                difference["position"] = position
                difference["reference_nucleotide"] = reference_nucleotide
                difference["variant_nucleotide"] = variant_nucleotide
                difference["chromosome"] = single_fasta.getChromosome()
                
                differences.append(difference)
        return differences
                
        
                
    def get_snp_by_positions(self, differences: list[dict], single_fasta: SingleFasta) -> list[Snp]:
        
        snp_refs: list[str] = []
        snps: list[Snp] = []
        
        Entrez.email = "test@test.com"
        specie_query: str = f"{single_fasta.getAssembly()}"
        snp_text_regexp = re.compile(r"=(\d+)$")
        
        try:
            handler = Entrez.esearch(db="assembly", term=specie_query)
            specie_id = Entrez.read(handler)["IdList"][0]
            specie_handler = Entrez.esummary(db = "assembly", id = specie_id)
            specie_summary = Entrez.read(specie_handler)
            specie_name = specie_summary["DocumentSummarySet"]["DocumentSummary"][0]["SpeciesName"]
            handler.close()
            print(differences)
            for difference in differences:
            
                snp_query: str = f"{difference['chromosome'].replace('chr','')}[CHR] AND {specie_name}[ORGN] AND {difference['position']}:{difference['position']}[CPOS]"
                handler = Entrez.esearch(db="snp",term=snp_query)
                record = Entrez.read(handler)
                ids = record["IdList"]
                
                #print(ids)
                
                handler.close()
                
                for id in ids:
                    snp_handler = Entrez.esummary(db = "snp", id = id)
                    snp_summary = Entrez.read(snp_handler)
                    snp_text = snp_summary["DocumentSummarySet"]["DocumentSummary"][0]["TEXT"]
                    snp_search = re.findall(snp_text_regexp,snp_text)
                    
                    found_snp = ""
                    if len(snp_search) > 0:
                        found_snp = f"rs{snp_search[0]}"
                    else:
                        found_snp: str = f"rs{id}"
                    
                    if found_snp not in snp_refs:
                        snp_refs.append(found_snp)
                        
            
                for i, snp_ref in enumerate(snp_refs):
                    
                    snp = Snp(ref_snp = snp_ref,
                            fasta_id = single_fasta.getFastaId(),
                            ref_nucleotide = differences[i]["reference_nucleotide"],
                            var_nucleotide = differences[i]["variant_nucleotide"]
                            )
                    
                    snps.append(snp)
                    
        except Exception as e:
            print(f"Get SNPS Handler: {e}")
        
        return snps


if __name__ == "__main__":
    pass
    
    # To run this example from file, a copy of Snp.py and SingleFasta.py must be placed in 
    # the same folder and uncomment the local import statments in header and please comment 
    # the server imports (module.)
    
    # The example returns Snp object with rs53576 identified.
    
    # # single_fasta_test: SingleFasta = SingleFasta(
    # #     1, 
    # #     'CTCGGGCACAGCATTCATGGAAAGGAAAGGTGTACGGGACATGCCCGAGGGTCCTCAGTCCCACAGAAACAGGGAGGGGCTGGGAAGCTCATTCTACAGATGGGG',
    # #     'hg38', 
    # #     'chr3',
    # #     1 , 
    # #     8762635, 
    # #     8762739
    # # )
    
    # # snp_handler: SnpHandler = SnpHandler()
    # # #assembly_exists: bool = snp_handler.check_if_assembly_exists("hg38")
    # # ref_seq: str = snp_handler.get_reference_sequence(single_fasta=single_fasta_test)
    
    # # differences = snp_handler.identify_differences(ref_seq,single_fasta_test)
    # # snps = snp_handler.get_snp_by_positions(differences, single_fasta_test)
    
    # # print(snps)
    
    
    