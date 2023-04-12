function loginFunction(body){

    axios
        .post('/api/users/login', body)
        .then(response => {
            console.log(response)
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