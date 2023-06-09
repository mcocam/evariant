/**
 * Code Summary:
 * This file contains functions to request and display data related to requests.
 */

/**
 * Retrieves a list of requests and samples in a table on the web page.
 */
function list_request() {
    // Show messages the user
    const snpMessage = $('#result-request');

    axios
        .get('/api/files/requests')
        .then(function (response) {
            // Format the response
            const request_snps = response.data.data;

            if (request_snps.length == 0) {
                $(snpMessage).html("<h3>Welcome to SNP Finder! It looks like you haven't performed a search yet,<br> search for SNP right now!</h3>");
            } else {

                request_snps.sort(function (a, b) {
                    return b[0] - a[0];
                });

                // CREATE TABLE request
                var thead = $("<thead><tr class='border-botton border-3' > <th scope='col'>ID</th> <th scope='col'>Date</th> <th scope='col'>Title</th><th></th><th></th></tr></thead>");

                var tbody = $("<tbody></tbody>");
                for (var i = 0; i < request_snps.length; i++) {
                    var row = $("<tr></tr>");
                    var rowData = request_snps[i];

                    // Add data to the table
                    row.append($("<td>" + rowData[0] + "</td>"));
                    row.append($("<td>" + rowData[4] + "</td>"));
                    row.append($("<td>" + rowData[1] + "</td>"));
                    row.append($("<td>" + "<button type='button' class='btn btn-default fw-bold fs-5 table-btn-style see-results-button'+ onclick='showResults(" + rowData[0] + ")'> See Results </button>" + "</td>"));
                    row.append($("<td>" + "<button type='button' class='btn btn-default fw-bold fs-5 table-btn-style' onclick='deleteFasta(" + rowData[0] + ")'> Delete </button>" + "</td>"));
                    tbody.append(row);
                }

                // Add the table header and body to the HTML page
                $("#table-request").append(thead);
                $("#table-request").append(tbody);

                // Display messages to the user based on the response from the server
                switch (response.data.message) {
                    case "915":
                        // Data obtained successfully
                        $(snpMessage).text('');
                        break;
                    case "914":
                        $(snpMessage).text('No results found');
                        break;
                    case "916":
                        $(snpMessage).text('Served has failed, try later');
                        break;
                    default:
                        $(snpMessage).text('');
                }

            }
        })
        .catch(e => {
            console.log(e);
        })
};
/**
 * Redirects the user to a page that displays the results of a request.
 * @param {number} fasta_id: the ID of the request whose results will be returned.
 */
function showResults(fasta_id) {
    window.location.href = "/request_results.html?fasta_id=" + fasta_id;
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
                window.location.href = './snp.html';
            })
            .catch(e => {
                console.log(e);
                return false;
            });
    }
}

$().ready(() => {
    // Call the list_request function when the document is ready
    list_request();
});