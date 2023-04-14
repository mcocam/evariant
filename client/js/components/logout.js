function logoutFunction(){

    // $.removeCookie('evariantSession');
    // document.cookie = 'evariantSession=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    Cookies.remove('evariantSession');

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

    $("#logoutButton").on("click", () => {
        console.log("Logging out")
        logoutFunction()
    });
});