from models.persist.FastaDao import FastaDao
from pydantic import BaseModel
from models.Fasta import Fasta
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


# Process Fasta
# Que todos sean nucleotides
# multi o simple
# Multi que tenga secuencia, insertar de una
# que tenga secuencia, ... y otros campos