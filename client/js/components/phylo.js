/**
 * Code Summary:
 * This code fetches phylogenetic requests from the server, populates a table with the data,
 * and provides functionality to view results or delete a request.
 */


/**
 * Function list_request_phylo
 * Fetches phylogenetic requests from the server, populates a table with the data, and handles messages.
 */
function list_request_phylo() {
    // Messages
    const phyloMessage = $('#result-phylo');

    axios
        .get('/api/phylo/requests')
        .then(function (response) {
            // Get data
            const requests_phylo = response.data.data;

            if (requests_phylo.length == 0) {
                $(phyloMessage).html("<h3>Turn multifasts into phylogenetic trees now! <br> Discover the fascinating evolutionary history of your data in one step.</h3>");
            } else {
                // Arrange the data in reverse order
                requests_phylo.sort(function (a, b) {
                    return b[0] - a[0];
                })

                // CREATE TABLE REQUEST PHYLO
                var thead = $("<thead><tr class='border-botton border-3' > <th scope='col'>ID</th> <th scope='col'>Date</th> <th scope='col'>Title</th><th></th><th></th></tr></thead>");

                var tbody = $("<tbody></tbody>");
                for (var i = 0; i < requests_phylo.length; i++) {
                    var row = $("<tr></tr>");
                    var rowData = requests_phylo[i];

                    //Add data to table
                    row.append($("<td>" + rowData[0] + "</td>"));
                    row.append($("<td>" + rowData[4] + "</td>"));
                    row.append($("<td>" + rowData[1] + "</td>"));
                    row.append($("<td>" + "<button type='button' class='btn btn-default fw-bold fs-5 table-btn-style see-results-button'+ onclick='showResults(" + rowData[0] + ")'> See Results </button>" + "</td>"));
                    row.append($("<td>" + "<button type='button' class='btn btn-default fw-bold fs-5 table-btn-style' onclick='deleteFasta(" + rowData[0] + ")'> Delete </button>" + "</td>"));
                    tbody.append(row);
                }

                // Add the table header and body to the HTML page
                $("#table-phylo").append(thead);
                $("#table-phylo").append(tbody);

                // Display messages to the user based on the response from the server
                switch (response.data.message) {
                    case "920":
                        //Data obtained successfully
                        $(phyloMessage).text('');
                        break;
                    case "921":
                        $(phyloMessage).text('No results found');
                        break;
                    case "922":
                        $(phyloMessage).text('Served has failed, try later');
                        break;
                    default:
                        $(phyloMessage).text('');
                }
            }
        })
        .catch(e => {
            console.log(e.message);
        })
};

/**
 * Function showResults
 * Redirects the user to a page that displays the results of a request.
 *
 * @param {number} fasta_id - The ID of the request whose results will be returned.
 */
function showResults(fasta_id) {
    window.location.href = "/phylo_results.html?fasta_id=" + fasta_id;
}

/**
 * Deletes the specified fasta.
 * @param {number} fasta_id: the ID of the fasta that will be deleted.
 */
function deleteFasta(fasta_id) {

    if (confirm('Are you sure you want to delete this fasta?')) {
        axios
            .get(`/api/files/delete_fasta/` + fasta_id)
            .then(response => {
                window.location.href = './trees.html';
            })
            .catch(e => {
                console.log(e);
                return false;
            });
    }
}

/**
 * Show Table
 */
$().ready(() => {
    // Call the list_request function when the document is ready
    list_request_phylo();
});