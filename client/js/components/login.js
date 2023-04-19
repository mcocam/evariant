/**
 * This function sends a POST request to the server to authenticate a user with the provided credentials.
 * @param {const} body 
 */
function loginFunction(body){
    
    const loginMessage = $('#result-login')
    loginMessage.empty();
    
    axios
        .post('/api/users/login', body)
        .then(response => {

            //If the request is successful, display a message to the user
            switch(response.data.message) {
                case "900":
                    $(loginMessage).text('Session On');
                    setTimeout(function() {
                        location.reload();
                      }, 1000);
                    break;
                case "904":
                    $(loginMessage).text('Invalid Credentials');
                    break;
                case "909":
                    $(loginMessage).text('Served has failed, try later');
                    break;
                default:
                    $(loginMessage).text('');
            }

        })
        .catch(e => {
            console.log(e);
        });

};


/** ---------------------- LOGIN ACTION ----------------------------- */

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
    });


});

/** ----------------------  ACTIVATE BUTTON ----------------------------- */

["#loginEmail", "#loginPassword"].forEach((i) => {
    $(i).on("change", () => {
        handleSignInButton()
    })
})

const handleSignInButton = () => {

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
