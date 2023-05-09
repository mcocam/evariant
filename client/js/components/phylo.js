/**
 * @authora Ani Valle
 */

function list_request_phylo(){
    // Messages
    const phyloMessage = $('#result-phylo');

    axios
    .get('/api/phylo/requests')
    .then(function(response) {
        // Get data
        const requests_phylo = response.data.data;
        // Arrange the data in reverse order
        requests_phylo.sort(function(a,b) {
            return b[0] - a[0];
        })

        // CREATE TABLE REQUEST PHYLO
        var thead = $("<thead><tr class='border-botton border-3' > <th scope='col'>ID</th> <th scope='col'>Date</th> <th scope='col'>Title</th> <th scope='col'></th><th scope='col'></th><th scope='col'></th></tr></thead>");

        var tbody =  $("<tbody></tbody>");
        for (var i = 0; i < requests_phylo.length; i++) {
            var row = $("<tr></tr>");
            var rowData = requests_phylo[i];

            //Add data to table
            row.append($("<td>" + rowData[0] + "</td>"));
            row.append($("<td>" + rowData[4] + "</td>"));
            row.append($("<td>" + rowData[1] + "</td>"));
            row.append($("<td>" + "<button type='button' class='btn btn-default fw-bold fs-5 table-btn-style'> Edit </button>"+ "</td>"));
            row.append($("<td>" + "<button type='button' class='btn btn-default fw-bold fs-5 table-btn-style see-results-button'+ onclick='showResults(" +rowData[0]+ ")'> See Results </button>"+ "</td>"));
            row.append($("<td>" + "<button type='button' class='btn btn-default fw-bold fs-5 table-btn-style'> Delete </button>"+ "</td>"));
            tbody.append(row);
        }

        // Add the table header and body to the HTML page
        $("#table-phylo").append(thead);
        $("#table-phylo").append(tbody);

        // Display messages to the user based on the response from the server
        switch(response.data.message) {
            case "920":
                //Data obtained successfully
                $(phyloMessage).text('');
                console.log(response.data.data);
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
    })
    .catch(e => {
        console.log(e.message);
    })
};


/**
 * Show 
 */
$().ready(() => {
    // Call the list_request function when the document is ready
    list_request_phylo();
});