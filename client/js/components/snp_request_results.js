$().ready(() => {

    const urlParams = new URLSearchParams(window.location.search);
    const fasta_id = urlParams.get('fasta_id');

    axios.get('/api/snp/results/' + fasta_id)
        .then(function (response) {
            const snps = response.data;
            
            const resultsBody = document.getElementById('results_body');

            for (let i = 0; i < snps.length; i++) {
                const snp = snps[i];
                const row = document.createElement('tr');
                const fastaId = document.createElement('td');
                const refNucleotide = document.createElement('td');
                const varNucleotide = document.createElement('td');
                fastaId.innerText = snp.fasta_id;
                refNucleotide.innerText = snp.ref_nucleotide;
                varNucleotide.innerText = snp.var_nucleotide;

                row.appendChild(fastaId);
                row.appendChild(refNucleotide);
                row.appendChild(varNucleotide);

                resultsBody.appendChild(row);
            }
        })
        .catch(function (error) {
            console.log(error);
            console.log('catch');
        });

});