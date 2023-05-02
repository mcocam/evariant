import re
from requests import get, Response
from models.persist.FastaDao import FastaDao
from models.utils.SnpHandler import SnpHandler

from pydantic import BaseModel
from models.Fasta import Fasta
import env
import os

class FastaController:

    def __init__(self) -> None:
        self.dao = FastaDao()
        self.snp_handler = SnpHandler()

    # ----------------------------------------------------------------
    async def get_fasta(self, id):

        data = None

        try:
            result = await self.dao.get_fasta_by_id(id)
            data = result

        except Exception as e:
            print(f"Get fasta info error: {e}")

        return data


    # ----------------------------------------------------------------
    async def add_fasta(self, new_fasta) -> int:

        new_fasta_added: int = 0

        try:
            new_fasta_added = self.dao.add_new_fasta(new_fasta)
        except Exception as e:
            print(e)

        return new_fasta_added
    

    # The function checks if it is a valid single FASTA
    # @Parameters fasta, a simple FASTA.
    async def is_valid_fasta(self, fasta):
        """ Receive a simple FASTA.
            Validates that it has the necessary data in the header.
            Validates that the sequence only contains valid nucleotide characters.

            Returns a tuple of 6 elements
            The first element indicates if the fasta is valid (True or False)
            """
        
        # Pattern to search in header
        header_pattern = r'^>([a-zA-Z0-9]+);(chr\d*);(1|2);(\d*:\d*)'
        match = re.search(header_pattern,fasta)
        if match:
            genome, chromosome, strand, position = match.group(1,2,3,4)
            
            splitted_fasta = fasta.split("\n")
            
            sequences = [line for line in splitted_fasta if len(re.findall(r">.*",line.strip())) == 0 and len(line) > 0 ]
            for seq in sequences:
                seq_temp = seq.replace(" ","").strip()
                invalid_nucleotides_search = re.findall("([^ATCGatcg])",seq_temp)
                
                if len(invalid_nucleotides_search) > 0:
                    return False, None, None, None, None, None

            # Validate that it has found the content in the header
            if genome and chromosome and strand and position:
                
                genome_exists: bool = self.snp_handler.check_if_assembly_exists(genome)
                
                if not genome_exists:
                    return False, None, None, None, None, None

                # Find the string on the line following the header
                sequence_pattern = r'\n([ACGTNacgtn\s]*)'
                match = re.search(sequence_pattern, fasta)
                if match:
                    sequence = match.group(1).replace('\n', '').replace(' ', '').upper()
                    # Verify that the sequence contains only valid nucleotide characters
                    if re.match(r"^[ACGT]+$", sequence):
                        return True, genome, chromosome, strand, position, sequence
            
        return False, None, None, None, None, None


    # The function checks if the file is a single fasta or a multi fasta
    # @param fasta
    # @return num_sequences: int, Return 0 if there is more than one sequence, 1 if there is only one
    async def get_type_fasta(self, fasta) -> int:

        # Separate the file into sequences
        sequences = fasta.split('>')[1:]
        # Count the number of sequences
        num_sequences = len(sequences)
        
        return 0 if num_sequences > 1 else 1
    

    # Get Info Fasta
    # @param user_id:int
    # @param type:int
    # @return data: list[list]
    #----------------------------------------------------------------
    async def get_fasta_info(self, user_id: int, single_fasta: int) :

        info_fasta: list[dict] = []
        data: list[str] = []

        try:
            # Get Info Fasta from DAO
            info_fasta: list[dict] =  await self.dao.get_info(user_id, single_fasta)
            # Convert to list of string
            data = [str(d) for d in info_fasta]
            #print(f"LLegan al controlador:  {data}")

        except Exception as e:
            print(f"FastaController Exception: {e}")
        return data