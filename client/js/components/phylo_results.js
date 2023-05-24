/**
 * Code Summary:
 * This code retrieves a FASTA ID from the URL parameters, sends a POST request to the server to fetch phylogenetic results,
 * and then displays the results by drawing a tree on the specified div element.
 */
$().ready(() => {

    // Retrieve the FASTA ID from the URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const fasta_id = urlParams.get('fasta_id');

    // Send a POST request to fetch phylogenetic results based on the FASTA ID
    axios.post('/api/phylo/results/' + fasta_id)
        .then(function (response) {
          // Extract the tree data from the response
            const tree = response.data.data.tree
            const div_id = "#see_results"

            // Draw the tree on the specified div element
            draw = drawTree(tree, div_id);

        })
        .catch(function (error) {
            console.log("Phylo catch error: " + error);
        });
})

/**
 * Function drawTree
 * Draws a phylogenetic tree on the specified div element.
 * @param {Object} tree - The tree data to be drawn.
 * @param {string} id - The ID of the div element where the tree will be drawn.
 */
const drawTree = (tree, id) => {
    const tree_canvas = new phylocanvas.PhylocanvasGL(
        document.querySelector(id),
          {
            size: { width: 500, height: 500 },
            showLabels: true,
            showLeafLabels: true,
            source: tree,
            type: phylocanvas.TreeTypes.Rectangular,
          },
        );
};