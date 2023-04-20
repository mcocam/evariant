from routes.fasta.fasta import router
from models.persist.FastaDao import FastaDao

fasta = FastaDao.get_fasta_by_id(1)
print(fasta)




