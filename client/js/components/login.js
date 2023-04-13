function loginFunction(body){

    axios
        .post('/api/users/login', body)
        .then(response => {
            console.log(response)
            if(response["error"] == true) {
                 $(function() {
                    $('result-login').text('A ocurrido un error');
                 });
            }else{
                $(function() {
                    $('result-login').text('Sin Errores');
                 });
            }
        })
        .catch(e => {
            console.log(e);
            return false;
        });


};

$().ready(() => {

    $("#loginButton").on("click", () => {
        const email     = $("#loginEmail").val();
        const password  = $("#loginPassword").val();

        const body = {
            "email": email, 
            "password": password
        };

        const response = loginFunction(body);
        //console.log(response);
    });

    //Login
    
    
});

function loginResponse() {

}