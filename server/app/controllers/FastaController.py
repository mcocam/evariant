from models.persist.FastaDao import FastaDao
from pydantic import BaseModel
from models.Fasta import Fasta
import re
import env
import os

class FastaController:

    def __init__(self) -> None:
        self.dao = FastaDao()

    # ----------------------------------------------------------------
    async def get_fasta(self, id):

        fasta = {}

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
    
    # ----------------------------------------------------------------
    async def validate_fasta(self, file_fasta):
        
        lines = file_fasta.decode().aplitlines()
        header = lines[0].strip()
        sequence = "".join(lines[1:]).replace("\n", "")

        if not header.startswith(">"):
            return False, "El encabezado del archivo no comienza con el símbolo '>'"
        
        if not ("assembly" in header and "chromosome" in header and "start" in header and "end" in header):
            return False, "El encabezado del archivo no contiene los campos assembly, chromosome, start y end"
        
        start_pos = re.search(r"start=(\d+)", header)
        end_pos = re.search(r"end=(\d+)", header)

        if not (start_pos or end_pos or start_pos):
            return False, "El encabezado del archivo no contiene información de inicio y finalización de la secuencia"

        start = int(start_pos.group(1))
        end = int(end_pos.group(1))

        if not re.match(r"^[ATCGatcg]+$", sequence):
            return False, "La secuencia del archivo contiene caracteres que no son 'A', 'T', 'C' o 'G'"
        
        return True, "El archivo .fasta es válido"


# Process Fasta
# Que todos sean nucleotides
# multi o simple
# Multi que tenga secuencia, insertar de una
# que tenga secuencia, ... y otros campos