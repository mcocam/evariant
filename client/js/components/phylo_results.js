
$().ready(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const fasta_id = urlParams.get('fasta_id');

    axios.post('/api/phylo/results/' + fasta_id)
        .then(function (response) {
            tree = response.data.data.tree
            div_id = "#see_results"

            draw = drawTree(tree, div_id);
            // const phylo = "Aquí se mostraran los results";

        })
        .catch(function (error) {
            console.log("Phylo catch error: " + error);
        });
})

const drawTree = (tree, id) => {
    const tree_canvas = new phylocanvas.PhylocanvasGL(
        document.querySelector(id),
          {
            size: { width: 400, height: 300 },
            showLabels: true,
            showLeafLabels: true,
            source: tree,
            type: phylocanvas.TreeTypes.Rectangular,
          },
        );
};