async function validateCookie() {

    let response = null;

    try {
        response = await fetch("./api/users/verify", {
            method: 'POST'
        })
        // console.log(response.status)
    } catch(e) {
        // console.log("tudo mal")
    }

    return await response.json();
};

const validSession = validateCookie();
console.log(validSession);