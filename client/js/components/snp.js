
function list_request(){

    const snpMessage = $('#result-request');

    axios
    .get('/api/files/requests')
    .then(function (response) {
        const snps = response.data;
        var finalList = [];

        for (let i = 0; i < snps.length; i++) { 
            let split = snps[i].split(", ");
            let innerList = [];

            for (let j = 0; j < split.length; j++) { 
                innerList.push(split[j]);
            }

            finalList.push(innerList);
        }

        // ya puedo crear la tabla
        console.log(finalList[1][1]);
        console.log("Mostrar request" + snps);
        console.log(response.data)


        // switch(response.data.message) {
        //     case "913":
        //         $(snpMessage).text('info', response.data);
        //         console.log(response.data)
        //         break;
        //     case "912":
        //         $(snpMessage).text('no se han encontrado resuntados');
        //         break;
        //     case "916":
        //         $(snpMessage).text('error de la exception');
        //         break;
        //     case "912":
        //         $(snpMessage).text('info');
        //         break;
        //     default:
        //         $(snpMessage).text('');
        //}
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