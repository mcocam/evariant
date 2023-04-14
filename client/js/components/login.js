function loginFunction(body){
    
    const loginMessage = $('#result-login')
    loginMessage.empty();
    
    axios
        .post('/api/users/login', body)
        .then(response => {
            console.log(response)

            if (response.data.message === "904"){
                $(loginMessage).text('Invalid Credentials text');
            }else if (response.data.message === "900"){
                $(loginMessage).text('Session On text');

            }

            // // Errores cogidos desde el error
            // if(response.data["error"] == true) {
            //     $('#result-login').text('Ha ocurrido un error');
            // }else{
            //     $('#result-login').text('Sin Errores');
            // }
        })
        .catch(e => {
            console.log(e);
        });

};



$().ready(() => {

    /** SEND CREDENTIALS TO SERVER */
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

/** ----------------------  ACTIVATE BUTTON ----------------------------- */

["#loginEmail", "#loginPassword"].forEach((i) => {
    $(i).on("change", () => {
        handleSingInButton()
    })
})

const handleSingInButton = () => {

    let state = [];

    ["#loginEmail", "#loginPassword"].forEach((input,index) => {
        const value = $(input).val();
            let isOk = false;

            if(index === 0){
                isOk = validateEmail();
            }else if(index === 1){
                isOk = validatePassword();
            }

        state.push(isOk);
    });

    if(state.some(data => data === false)){
        // Desactivar
        $('#loginButton').prop('disabled', true);

    }else{
        // Activar
        $('#loginButton').prop('disabled', false);

    }

}

/** -------------------------------- VALIDATION FUNCTIONS ------------------------ */


// Validate email format and length
function validateEmail() {

    // Collect Valued email
    email = $("#loginEmail").val();

    // Regext Validate Email
    var regex = new RegExp(/^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/);
    
    if (regex.test(email) && email.length <= 50) {
        $("#msgEmail").html("");
        return true; // No hay errores
    }else{
        $("#msgEmail").html("<p>Wrong email format entered</p>");
        return false; // Hay errores
    }
}

// Validate Password format and length
function validatePassword() {

    // Collect Valued Password
    psw  = $("#loginPassword").val();

    // Regext Validate Password
    var regex = new RegExp(/^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{8,16}$/);
    if (regex.test(psw)) {
        $("#msgPsw").html("");
        return true; // No hay errores
    }else{
        $("#msgPsw").html("<p>The password must have between 8 and 16 characters, at least one digit, at least one lower case and at least one upper case.</p>")
        return false; // Hay errores
    }

}
