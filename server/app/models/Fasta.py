# Class Fasta
# @author: Ani Valle

from datetime import datetime

class Fasta:

    def __init__(self,
                 title:     str,
                 raw_fasta: str,
                 type:      int,
                 user_id:   int,
                 id:        int = None,
                 creation_date: datetime = None,
                 ) -> None:
        
        self.title = title
        self.raw_fasta = raw_fasta
        self.type = type
        self.user_id = user_id
        self.id = id
        self.creation_date = creation_date

    # GETTERS
    def get_title(self) -> str:
        return self.title
    
    def get_raw_fasta(self) -> str:
        return self.raw_fasta

    def get_type(self) -> int:
        return self.type

    def get_user_id(self) -> int:
        return self.user_id
    
    def get_id(self) -> int:
        return self.id
    
    def get_creation_date(self) -> datetime:
        return self.get_creation_date

    # SETTERS
    def set_title(self, title: str) -> None:
        self.title = title

    def set_raw_fasta(self, raw_fasta: str) -> None:
        self.raw_fasta = raw_fasta

    def set_type(self, type: int) -> None:
        self.type = type

    def set_user_id(self, user_id: int) -> None:
        self.user_id = user_id

    def set_id(self, id: int) -> None:
        self.id = id


