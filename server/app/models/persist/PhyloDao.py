from models.PhyloTree import PhyloTree
from db.get_connection import get_connection
from sqlalchemy import Table, MetaData, Column, String, insert, select, and_
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
        
    def get_phylo_by_fasta_id(self, fasta_id: int) -> list[PhyloTree] | list:
        
        phylos: list = []
        
        try:
            query_phylo = self.phylo_table.select().where(self.phylo_table.c.fasta_id == fasta_id)
            query_fasta = select(self.fasta_table.c.user_id).where(self.fasta_table.c.id == fasta_id)
            
            cursor = self.connection.connect()
            phylo_row = cursor.execute(query_phylo).fetchone()
            fasta_row = cursor.execute(query_fasta).fetchone()
            
            phylo = PhyloTree(phylo_row[1],fasta_row[0],phylo_row[0])
            
            phylos.append(phylo)
            
        except Exception as e:
            print(f"Phylo DAO get by fasta_id: {e}")
            
        return phylos
    
    def get_phylos_by_user_id(self, user_id: int) -> list[PhyloTree] | list:
        
        phylos: list = []
        
        try:
            
            cursor = self.connection.connect()
            
            fasta_id_query = select(self.fasta_table.c.id).where(and_(self.fasta_table.c.user_id == user_id, self.fasta_table.c.type == 0))
            fasta_id_response = cursor.execute(fasta_id_query).fetchall()
            fastas_id = [id[0] for id in fasta_id_response]
                
            if len(fastas_id) > 0:
                
                user_phylos_query = self.phylo_table.select().where(self.phylo_table.c.fasta_id.in_(fastas_id))
                
                user_phylos = cursor.execute(user_phylos_query).fetchall()
                
                for phylo in user_phylos:
                    phylo_parsed = PhyloTree(phylo[1],user_id,phylo[0])
                    phylos.append(phylo_parsed)
            
        except Exception as e:
            print(f"Phylo DAO get by user_id: {e}")
            
        return phylos

