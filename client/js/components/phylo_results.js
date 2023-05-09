$().ready(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const fasta_id = urlParams.get('fasta_id');

    axios.get('/api/phylo/results/' + fasta_id)
        .then(function (response) {
            const phylo = response.data;

            const phyloResults = document.getElementById('see_results');
            $(snpMessage).text(phylo);

        })
        .catch(function (error) {
            console.log("Phylo catch" + error);
        });
})