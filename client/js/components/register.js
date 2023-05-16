/**
 * Code Summary:
 * This file contains the process to register a new user to the web.
 * Validates each input and shows comments to the user, if they are correct,
 * activate the button and let the user register.
 */


/**
 * This function sends a POST request to the server to create and store a new user in the database with the provided info.
 * @param {const} body - The user data to be sent to the server.
 */
function registerFunction(body) {

    const registerMessage = $('#result-register')
    registerMessage.empty();

    axios
        .post('/api/users/register', body)
        .then(response => {
            //Display a message to the user
            switch (response.data.message) {
                case "900":
                    $(registerMessage).html('<p class="text-center fw-bold text-success">User created successfully<p>');
                    setTimeout(function () {
                        window.location.href = './index.html?modal=true';
                    }, 500);
                    break;
                case "902":
                    $(registerMessage).html('<p class="text-center fw-bold text-danger">User already exists</p>');
                    break;
                case "909":
                    $(registerMessage).text('<p class="text-center fw-bold text-warning">Served has failed, try later</p>');
                    break;
                default:
                    $(registerMessage).text('');
            }
        })
        .catch(e => {
            console.log(e);
            return false;
        });
};

/** ---------------------- REGISTER ACTION ----------------------------- */

/**
 * Handles the click event of the register button and calls the registerFunction to register a new user.
 */
$().ready(() => {

    $("#registerButton").on("click", () => {
        const name = $("#registerName").val();
        const surname = $("#registerSurname").val();
        const email = $("#registerEmail").val();
        const password = $("#registerPassword").val();

        const body = {
            "email": email,
            "password": password,
            "name": name,
            "surname": surname
        };

        const response = registerFunction(body);
        //console.log(response);
    });

});

/** ----------------------  ACTIVATE BUTTON ----------------------------- */

/**
 * Handles the change event of the input fields and enables/disables the register button based on the input validity.
 */
["#registerName", "#registerSurname", "#registerEmail", "#registerPassword"].forEach((i) => {
    $(i).on("change", () => {
        handleRegisterButton()
    })
})

/**
 * Enables or disables the register button based on the validity of the input fields.
 */
const handleRegisterButton = () => {

    let state = [];

    ["#registerName", "#registerSurname", "#registerEmail", "#registerPassword"].forEach((input, index) => {
        const value = $(input).val();
        let isOk = false;

        if(index === 0){
            isOk = validateName();
        }else if(index === 1){
            isOk = validateSurname();
        }else if(index === 2){
            isOk = validateEmail();
        }else if(index === 3){
            isOk = validatePassword();
        }

        state.push(isOk);
    });

    if (state.some(data => data === false)) {
        // Disable register button
        $('#registerButton').prop('disabled', true);
    } else {
        // Enable register button
        $('#registerButton').prop('disabled', false);
    }

    /** -------------------------------- VALIDATION FUNCTIONS ------------------------ */

    /**
     * Validation Functions:
     * Validate the format and length of name, surname, email, and password inputs.
     */
    function validateName() {

        // Collect input Name
        nam = $("#registerName").val();
        // Regex Validate Name
        var regex = new RegExp(/^[a-zA-ZÀ-ÖØ-öø-ÿ]+(?:[' -][a-zA-ZÀ-ÖØ-öø-ÿ]+)*$/);

        if (regex.test(nam) && nam.length <= 50) {
            $("#msgName").html("");
            return true;
        } else {
            $("#msgName").html("<p>Wrong name format entered</p>");
            return false;
        }
    }

    // Validate surname format and length
    function validateSurname() {

        // Collect input Surname
        var surname = $("#registerSurname").val();
        // Regex Validate Surname
        var regex = new RegExp(/^[a-zA-ZÀ-ÖØ-öø-ÿ]+(?:[' -][a-zA-ZÀ-ÖØ-öø-ÿ]+)*$/);

        if (regex.test(surname) && surname.length <= 50) {
            $("#msgSurname").html("");
            return true;
        } else {
            $("#msgSurname").html("<p>Wrong surname format entered</p>");
            return false;
        }
    }
    
    // Validate email format and length
    function validateEmail() {

        // Collect Valued email
        email = $("#registerEmail").val();
        // Regext Validate Email
        var regex = new RegExp(/^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/);

        if (regex.test(email) && email.length <= 50) {
            $("#msgEmailRegister").html("");
            return true;
        } else {
            $("#msgEmailRegister").html("<p>Wrong email format entered</p>");
            return false;
        }
    }

    // Validate Password format and length
    function validatePassword() {

        // Collect Valued Password
        psw = $("#registerPassword").val();
        // Regext Validate Password
        var regex = new RegExp(/^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{8,16}$/);
        if (regex.test(psw)) {
            $("#msgPswRegister").html("");
            return true; // No hay errores
        } else {
            $("#msgPswRegister").html("<p>The password must have between 8 and 16 characters, at least one digit, at least one lower case and at least one upper case.</p>")
            return false; // Hay errores
        }
    }
}