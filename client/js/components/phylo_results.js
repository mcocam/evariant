
$().ready(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const fasta_id = urlParams.get('fasta_id');
    const phyloResults = document.getElementById('see_results');

    axios.post('/api/phylo/results/' + fasta_id)
        .then(function (response) {
            xml = response.data.data.tree

            draw = drawTree(xml);
            // const phylo = "Aquí se mostraran los results";
            phyloResults.appendChild(draw);

        })
        .catch(function (error) {
            console.log("Phylo catch error: " + error);
        });
})

const drawTree = (xml) => {
    const parser = new DOMParser();
    const doc = parser.parseFromString(xml, "text/xml");
    const svg = build(makeCompatTable(phyloxml.parse(doc)));
    return svg.node();
};