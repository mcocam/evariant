# from models.persist.FastaDao import FastaDao
from models.persist.SingleFastaDao import SingleFastaDao
from pydantic import BaseModel
from models.Fasta import Fasta
from models.SingleFasta import SingleFasta
import env
import os


class SingleFastaController:
    def __init__(self) -> None:
        self.dao = SingleFastaDao()

    def parse_single_fasta(self, fasta: Fasta) -> SingleFasta:
        raw = fasta.get_raw_fasta()
        seq = "".join(raw.split("\n")[1:])
        seq = seq.replace(" ", "").replace("\t", "")
        first_line = raw.split('\n')[0][1:]
        sections = first_line.split(';')    # assembly;chromosome;strand;positions;
        positions = sections[3].split("-")

        sf = SingleFasta(fasta.get_id(), seq, sections[0], sections[1], sections[2], positions[0], positions[1])

        self.dao.add_new_single_fasta(sf)
