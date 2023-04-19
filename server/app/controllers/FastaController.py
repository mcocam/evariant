from models.persist.FastaDao import FastaDao
from pydantic import BaseModel
from models.Fasta import Fasta
import env
import os

class FastaController:

    def __init__(self) -> None:
        self.dao = FastaDao()

    async def add_fasta(self, new_fasta) -> bool:

        new_fasta_added: bool = False

        try:
            new_fasta_added = self.dao.add_new_fasta(new_fasta)
        except Exception as e:
            print(e)

        return new_fasta_added