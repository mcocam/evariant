function loginFunction(body){

    axios
        .post('/api/users/login', body)
        .then(response => {
            // console.log(response)

            if (response.message[904]){
                $('#result-login').text('Invalid Credentials');
            }else if (response.message[900]){
                $('#result-login').text('Session On');
            }


            // Errores cogidos desde el error
            if(response.data["error"] == true) {
                $('#result-login').text('Ha ocurrido un error');
            }else{
                $('#result-login').text('Sin Errores');
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

});
