function registerFunction(body){

    axios
        .post('/api/users/register', body)
        .then(response => {
            console.log(response)
        })
        .catch(e => {
            console.log(e);
            return false;
        });


};

$().ready(() => {

    $("#registerButton").on("click", () => {
        const name      = $("#registerName").val();
        const surname   = $("#registerSurname").val();
        const email     = $("#registerEmail").val();
        const password  = $("#registerPassword").val();

        const body = {
            "email":    email, 
            "password": password,
            "name":     name,
            "surname":  surname
        };

        const response = registerFunction(body);
        //console.log(response);
    });
    
});