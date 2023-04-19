from pydantic import BaseModel, validator
import re

class New_fasta(BaseModel):

    title:     str
    raw_fasta: str
    type:      int
    user_id:   int
    
    pass




