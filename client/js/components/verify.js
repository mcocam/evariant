
//Validates the user's session cookie by sending a POST request to the server.
//@returns {Promise<Response>} A promise that resolves to the response of the server.
 
async function validateCookie() {

    try {
        const response = await fetch("./api/users/verify", {
            method: 'POST'
        })
        return response;
    } catch(e) {
        // console.log("Verify cookie failed: " e)
    }
};

// Call the validateCookie function and store the promise in validSession
let validSession = validateCookie();