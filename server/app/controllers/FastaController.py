import re
from requests import get, Response
# from models.persist.FastaDao import FastaDao
# from models.utils.SnpHandler import SnpHandler

from pydantic import BaseModel
# from models.Fasta import Fasta
# import env
import os

class FastaController:

    # def __init__(self) -> None:
    #     self.dao = FastaDao()

    # # ----------------------------------------------------------------
    # async def get_fasta(self, id):

    #     data = {}

    #     try:
    #         result = self.dao.get_fasta_by_id(id)
    #         data = list(result[0])

    #     except Exception as e:
    #         print(f"Get fasta info error: {e}")

    #     return data


    # # ----------------------------------------------------------------
    # async def add_fasta(self, new_fasta) -> bool:

    #     new_fasta_added: bool = False

    #     try:
    #         new_fasta_added = self.dao.add_new_fasta(new_fasta)
    #     except Exception as e:
    #         print(e)

    #     return new_fasta_added
    
    # # ----------------------------------------------------------------
    # async def validate_fasta(self, file_fasta: str) -> str:

    #     """ This regular expression requires the string to start with the '>'
    #         It contains 5 groups, g1 extracts the reference genome, g2 the chromosome,
    #         g3 the strand, g4 the positions, g5 the sequence. """
    #     # Regex setup
    #     reg: str = r'[^>]([a-zA-Z0-9]+);(chr\d*);(1|2);(\d*:\d*)\\n([A|T|C|G|a|t|c|g|\\n|\s]*)'
    #     pat: re.Pattern = re.compile(reg)

    #     #Get matches
    #     match_list: list[re.Match] = list(pat.finditer(file_fasta))

    #     # Return list of matches (fasta) as strings
    #     # Obtener cada parte del fasta y convertirlo en un objeto
        
    #     fasta_list: list[str] = [match.group(1) for match in match_list]

    #     return fasta_list

    #     pass

    def is_valid_fasta(self, fasta):
    # Buscar el patrón
        header_pattern = r'^>([a-zA-Z0-9]+);(chr\d*);(1|2);(\d*:\d*)'
        match = re.search(header_pattern,fasta)
        if match:
            genome, chromosome, strand, position = match.group(1,2,3,4)

            #Validar que ha encontrado el contenido en el header
            if genome and chromosome and strand and position:
                # Buscamos la secuencia en la línea siguiente al encabezado
                sequence_pattern = r'\n([ACGTNacgtn\s]*)'
                match = re.search(sequence_pattern, fasta)
                if match:
                    sequence = match.group(1).replace('\n', '').replace(' ', '').upper()
                    # Verificar que la secuencia solo contenga caracteres válidos de nucleótidos
                    if re.match(r"^[ACGT]+$", sequence):
                        return True, genome, chromosome, strand, position, sequence
            
        return False, None, None, None, None, None


    # Validar si es un fasta simple
    def is_fasta_s_m(self, text):
        sequences = text.split(">")[1:]
        for sequence in sequences:
            if "\n>" in sequence:
                return 0
        return 1 if sequences else False


# Pruebas
if __name__ == '__main__':
    fasta = '>hg38;chr3;1;8762635:8762739\nCTCGGGCACAGCATTCATGGAAAGGAAAGGTGTACGGGACATGCCCGAGGATCCTCAGTCCCACAGAAAC AGGGAGGGGCTGGGAAGCTCATTCTACAGATGGGG\n>'
    fasta_incorrect = '>GRCh38;1;1:50\natgatacacgcgggcgaccgcgcagtcaaYcttcaacatgtaaccctagacgccctgaat\nagctatgtccacacttcctcatttctgcctcccagataccagagcccgcggcgttgggct\ncacataccagaattccScgttcttacctaa'
    
    fastaC: FastaController = FastaController()
    
    # Tipo de fasta
    type_fasta = fastaC.is_fasta_s_m(fasta)

    print(type_fasta)

    if type_fasta == 1 :

        is_fasta, genome, chromosome, strand, position, sequence = fastaC.is_valid_fasta(fasta)
        if is_fasta:
            print(f"Fasta Semple. Genoma de reference:{genome} Chromosome: {chromosome} Hebra: {strand} y las posiciones: {position}")
            print(f"Secuencia: {sequence}")
        else:
            print("No es un archivo fasta simple válido.")
    elif type_fasta == 0:
        print("Es un multi fasta")
    else:
        print("No es un formato fasta valido5")


# Process Fasta
# Que todos sean nucleotides
# multi o simple
# Multi que tenga secuencia, insertar de una
# que tenga secuencia, ... y otros campos