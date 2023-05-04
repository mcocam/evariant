async function validateCookie() {


    try {
        const response = await fetch("./api/users/verify", {
            method: 'POST'
        })
        return response;
        // console.log(response.status)
    } catch(e) {
        // console.log("tudo mal")
    }
};

const validSession = validateCookie();