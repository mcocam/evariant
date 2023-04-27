
function list_request(){

    const snpMessage = $('#result-request');

    axios
    .post('/api/files//request_fastas')
    .then(response => {
        switch(response.data.message) {
            case "913":
                $(snpMessage).text('info', response.data.data.info);
                console.log(response.data)
                break;
            case "912":
                $(snpMessage).text('no se han encontrado resuntados');
                break;
            case "916":
                $(snpMessage).text('error de la exception');
                break;
            case "912":
                $(snpMessage).text('info');
                break;
            default:
                $(snpMessage).text('');
        }
    })
    .catch(e => {
        console.log(e);
    })
};



$().ready(() => {
    $('#btn-request').on('click', () => {
        
        list_request();
    });
})