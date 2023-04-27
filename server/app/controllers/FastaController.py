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

    # ----------------------------------------------------------------
    async def get_fasta(self, id):

        data = {}

        try:
            result = self.dao.get_fasta_by_id(id)
            data = list(result[0])

        except Exception as e:
            print(f"Get fasta info error: {e}")

        return data


    # ----------------------------------------------------------------
    async def add_fasta(self, new_fasta) -> bool:

        new_fasta_added: bool = False

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

            # Validate that it has found the content in the header
            if genome and chromosome and strand and position:

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
    async def get_type_fasta(self, fasta) -> int:

        # Separar el archivo en secuencias
        sequences = fasta.split('>')[1:]
        # Contar el número de secuencias
        num_sequences = len(sequences)
        
        # Devolver 0 si hay más de una secuencia, 1 si hay una sola
        return 0 if num_sequences > 1 else 1







# Pruebas
# if __name__ == '__main__':
#     fasta = '>hg38;chr3;1;8762635:8762739\nCTCGGGCACAGCATTCATGGAAAGGAAAGGTGTACGGGACATGCCCGAGGATCCTCAGTCCCACAGAAAC AGGGAGGGGCTGGGAAGCTCATTCTACAGATGGGG'
#     fasta_incorrect = '>GRCh38;1;1:50\natgatacacgcgggcgaccgcgcagtcaaYcttcaacatgtaaccctagacgccctgaat\nagctatgtccacacttcctcatttctgcctcccagataccagagcccgcggcgttgggct\ncacataccagaattccScgttcttacctaa'
#     multi_fasta = '>random coding sequence 9 consisting of 300 bases.\natgatctgtcttcttccctccgtgcacatgcgttgcatgtatatagcatcaatacccttt\ntgttccactaatgtggcggtgcatgaggctgttcgcatgagccgtatacagcgattcttg\naatttggagtacaaaacaatggaacccccatatagaactccgaataccatatcctgcatt\nggcggaaggaacccgtgggcacggtctcccttacgaagctacttaagaatgcttggcaaa\ntcgtgctatcctctgcgagagagtatcaggtcaattcaactcgtttcctctattccctag\n\n>random coding sequence 10 consisting of 300 bases.\natgagacactccgtaatttccagcaagacgaatt'
    
#     fastaC: FastaController = FastaController()
    
#     # Tipo de Fasta
#     type_fasta = fastaC.get_type_fasta(fasta)

#     print(f"Tipo de fasta: {type_fasta}")

#     if type_fasta == 1 :

#         is_fasta, genome, chromosome, strand, position, sequence = fastaC.is_valid_fasta(fasta)
#         if is_fasta:
#             print(f"Fasta Semple. Genoma de reference:{genome} Chromosome: {chromosome} Hebra: {strand} y las posiciones: {position}")
#             print(f"Secuencia: {sequence}")
#         else:
#             print("No es un archivo fasta simple válido.")
#     elif type_fasta == 0:
#         print("Es un multi fasta")
#     else:
#         print("No es un formato fasta valido5")


# Process Fasta
# Que todos sean nucleotides
# multi o simple
# Multi que tenga secuencia, insertar de una
# que tenga secuencia, ... y otros campos