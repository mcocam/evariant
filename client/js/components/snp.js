
function list_request(){

    const snpMessage = $('#result-request');

    axios
    .get('/api/files/requests')
    .then(function (response) {
        // Format the response
        const request_snps = response.data.data;
        console.log("Mostrar request" + request_snps);

        // CREATE TABLE request
        var thead = $("<thead><tr class='border-botton border-3' > <th>ID</th> <th>Date</th> <th>Title</th> <th></th><th></th><th></th></tr></thead>");

        var tbody = $("<tbody></tbody>");
        for (var i = 0; i < request_snps.length; i++) {
            var row = $("<tr></tr>");
            var rowData = request_snps[i];

            // Agregar las columnas de datos
            row.append($("<td>" + rowData[0] + "</td>"));
            row.append($("<td>" + rowData[4] + "</td>"));
            row.append($("<td>" + rowData[1] + "</td>"));
            row.append($("<td>" + "<button type='button' class='btn btn-default fw-bold fs-5 table-btn-style'> Edit </button>"+ "</td>"));
            row.append($("<td>" + "<button type='button' class='btn btn-default fw-bold fs-5 table-btn-style see-results-button'+ onclick='showResults(2)'> See Results </button>"+ "</td>"));
            row.append($("<td>" + "<button type='button' class='btn btn-default fw-bold fs-5 table-btn-style'> Delete </button>"+ "</td>"));
            tbody.append(row);
        }

        $("#table-request").append(thead);
        $("#table-request").append(tbody);


        // Mostrar informacion al usuario
        switch(response.data.message) {
            case "912":
                console.log(response.data.data)
                break;
            case "911":
                $(snpMessage).text('No results found');
                break;
            case "913":
                $(snpMessage).text('error de la exception');
                break;
            default:
                $(snpMessage).text('');
        }

    })
    .catch(e => {
        console.log(e);
    })
};

function showResults(fasta_id) {
    window.location.href = "/request_results.html?fasta_id=" + fasta_id;
}

$().ready(() => {

    list_request();
    
});