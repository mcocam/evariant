function logoutFunction(){

    $.cookie("evariantSession", null, { path: '/' });

    axios
        .post('/api/users/logout')
        .then(response => {
            console.log(response)
        })
        .catch(e => {
            console.log(e);
            return false;
        });


};

$().ready(() => {
    console.log("Logout ready")

    $("#logoutButton").on("click", () => {
        console.log("Logging out")
        logoutFunction()
    });
});