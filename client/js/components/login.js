/**
 * This function sends a POST request to the server to authenticate a user with the provided credentials.
 * @param {const} body 
 */
function loginFunction(body){
    
    const loginMessage = $('#result-login')
    loginMessage.empty();
    
    // Send a POST request to the server for user login
    axios
        .post('/api/users/login', body)
        .then(response => {

            // Display a message to the user based on the server response
            switch(response.data.message) {
                case "900":
                    $(loginMessage).html('<p class="text-center fw-bold text-success">Session On<p>');
                    setTimeout(function() {
                        window.location.href = './index.html';
                      }, 500);
                    break;
                case "904":
                    $(loginMessage).html('<p class="text-center fw-bold text-danger">Invalid Credentials</p>');
                    break;
                case "909":
                    $(loginMessage).text('<p class="text-center fw-bold text-warning">Served has failed, try later</p>');
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

        // Create the body object with email and password
        const body = {
            "email": email, 
            "password": password
        };

        // Call the loginFunction and pass the body object
        const response = loginFunction(body);
    });


});

/** ----------------------  ACTIVATE BUTTON ----------------------------- */

// Event listeners for input changes on email and password fields
["#loginEmail", "#loginPassword"].forEach((i) => {
    $(i).on("change", () => {
        handleSignInButton()
    })
})

// Function to handle the state of the sign-in button
const handleSignInButton = () => {

    let state = [];

    // Validate email and password inputs
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
        // Disable the sign-in button
        $('#loginButton').prop('disabled', true);

    }else{
        // Enable the sign-in button
        $('#loginButton').prop('disabled', false);
    }

}

/** -------------------------------- VALIDATION FUNCTIONS ------------------------ */

// Validate email format and length
function validateEmail() {

    // Collect the entered email
    email = $("#loginEmail").val();

    // Regular expression to validate email format
    var regex = new RegExp(/^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/);
    
    if (regex.test(email) && email.length <= 50) {
        $("#msgEmail").html("");
        return true; // No errors
    }else{
        $("#msgEmail").html("<p>Wrong email format entered</p>");
        return false; // Errors
    }
}

// Validate Password format and length
function validatePassword() {

    // Collect the entered password
    psw  = $("#loginPassword").val();

    // Regular expression to validate password format
    var regex = new RegExp(/^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{8,16}$/);
    if (regex.test(psw)) {
        $("#msgPsw").html("");
        return true; // No errors
    }else{
        $("#msgPsw").html("<p>The password must have between 8 and 16 characters, at least one digit, at least one lower case and at least one upper case.</p>")
        return false; // Errors
    }
}
