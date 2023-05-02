
function list_request(){

    const snpMessage = $('#result-request');

    axios
    .get('/api/files/requests')
    .then(function (response) {

        
        // Format the response
        const request_snps = response.data.data;
        var requestList = [];

        for (let i = 0; i < request_snps.length; i++) { 
            let splitList = request_snps[i].split(", ");
            let innerList = [];

            for (let j = 0; j < splitList.length; j++) {
                // if (j === 4){
                //     let date = new Date(splitList[j]);
                //     let dateString = `${date.getFullYear().toString()}-${date.getMonth() + 1}-${date.getDate()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
                //     innerList.push(dateString);
                // } else {
                innerList.push(splitList[j]);
            }
            
            let dateString = innerList[4].replace('datetime.datetime(','') +','+innerList[5]+','+innerList[6];
            console.log("date String  "+ innerList[4].replace('datetime.datetime(',''));

            let date = new Date(parseInt(dateString));
            innerList[4] = date.toLocaleString();

            requestList.push(innerList);
        }

        // Ya puedo crear la tabla
        console.log("Request List "+requestList[1][4]);
        console.log("Mostrar request" + request_snps);

        // Create Tabla
        var thead = $("<thead><tr border-botton border-3 ><th col>ID</th><th col >Date</th><th col >Title</th></tr></thead>");

        var tbody = $("<tbody></tbody>");
        for (var i = 0; i < requestList.length; i++) {
            var row = $("<tr></tr>");
            var rowData = requestList[i];

            // Agregar las columnas de datos
            row.append($("<td>" + rowData[0] + "</td>"));
            row.append($("<td>" + rowData[4] + "</td>"));
            row.append($("<td>" + rowData[1] + "</td>"));

            tbody.append(row);
        }

        $("#table-request").append(thead);
        $("#table-request").append(tbody);


        

        // Mostrar informacion al usuario
        switch(response.data.message) {
            case "912":
                $(snpMessage).text('info', request_snps);
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

    $('#btn-request').on('click', () => {
        list_request();
    });
    
});