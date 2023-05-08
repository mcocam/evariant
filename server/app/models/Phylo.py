

class Phylo:
    
    def __init__(self,
                 fasta_id: int,
                 user_id: int,
                 xml: str
                 ) -> None:
        
        self.fasta_id   = fasta_id
        self.user_id    = user_id,
        self.xml        = xml
        
    def get_fasta_id(self) -> int:
        return self.fasta_id 
    
    def get_user_id(self) -> int:
        return self.user_id
    
    def get_xml(self) -> str:
        return self.xml 
    
    def set_fasta_id(self, fasta_id: int) -> None:
        self.fasta_id = fasta_id
        
    def set_user_id(self, user_id: int) -> None:
        self.user_id = user_id
        
    def set_xml(self, xml: str) -> None:
        self.xml = xml