from models.persist.FastaDao import FastaDao
# from models.persist.FastaDao import SingleFastaDao << TODO
from pydantic import BaseModel
from models.Fasta import Fasta
# from models.Fasta import SingleFasta << TODO
import env
import os

class SingleFastaController:

    def __init__(self) -> None:
        self.dao = FastaDao()
        # self.dao = SingleFastaDao() << TODO



# Process Fasta
# Que todos sean nucleotides
# multi o simple
# Multi que tenga secuencia, insertar de una
# que tenga secuencia, ... y otros campos