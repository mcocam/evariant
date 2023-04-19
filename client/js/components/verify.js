async function validateCookie() {


    try {
        const response = await fetch("./api/users/verify", {
            method: 'POST'
        })
        const text = await response.json();
        return text;
        // console.log(response.status)
    } catch(e) {
        // console.log("tudo mal")
    }
};

const validSession = validateCookie();
validSession.then(d => {
    if(d.status_code === 200){
        console.log("Session ok!")
    }else{
        console.log("Session Off!")
    }
});