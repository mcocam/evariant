from models.Phylo import Phylo
from db.get_connection import get_connection
from sqlalchemy import Engine, Table, MetaData, Column, Integer, String, DateTime, insert
from models.persist.FastaDao import fasta_table

phylo_table: Table = Table(
    "clusters",
    MetaData(),
    Column("phylo_xml"),
    Column("fasta_id")
)


class PhyloDao:
    
    def __init__(self) -> None:
        self.connection = get_connection()
        self.fasta_table = fasta_table
        self.phylo_table = phylo_table
        
    def get_phylo_by_fasta_id(self, fasta_id: int) -> list[Phylo] | list:
        
        phylos: list = []
        
        try:
            query_phylo = self.phylo_table.select().where(self.phylo_table.c.fasta_id == fasta_id)
            query_fasta = self.fasta_table.select([self.fasta_table.c.user_id]).where(self.fasta_table.c.id == fasta_id)
            
            cursor = self.connection.connect()
            phylo_row = cursor.execute(query_phylo).fetchone()
            fasta_row = cursor.execute(query_fasta).fetchone()
            
            phylo = Phylo(phylo_row[1],phylo_row[0],fasta_row[0])
            
            phylos.append(phylo)
            
        except Exception as e:
            print(f"Phylo DAO get by fasta_id: {e}")
            
        return phylos
