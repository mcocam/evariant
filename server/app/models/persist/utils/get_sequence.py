from Bio import Entrez, SeqIO

Entrez.email = "evariant@evariants.com"

handler = Entrez.esearch(db="nucleotide",term="GRCh38.p14 Primary Assembly",retmax=5)
record = Entrez.read(handler)
ids = record["IdList"]
# # print(ids)

for id in ids:
    summary_handler = Entrez.esummary(db="nucleotide",id=id)
    summary_record = Entrez.read(summary_handler)

    print(summary_record)

# handle = Entrez.efetch(db="nucleotide", 
#                        id="307603377", 
#                        rettype="fasta", 
#                        strand=1, 
#                        seq_start=4000100, 
#                        seq_stop=4000200)
# record = SeqIO.read(handle, "fasta")
# handle.close()
# print(record.seq)