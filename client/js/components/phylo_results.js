$().ready(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const fasta_id = urlParams.get('fasta_id');

    axios.post('/api/phylo/results/' + fasta_id)
        .then(function (response) {
            xml = response.data.data.xml
            console.log(response.data.data.xml);
            
            
            // const phylo = "Aquí se mostraran los results";
            // const phyloResults = document.getElementById('see_results');
            // $(phyloResults).text(phylo);

        })
        .catch(function (error) {
            console.log("Phylo catch " + error);
        });
})