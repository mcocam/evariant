function logoutFunction(){

    axios
        .post('/api/users/logout')
        .then(response => {
            console.log(response)
            location.reload();
        })
        .catch(e => {
            console.log(e);
            return false;
        });


};

$().ready(() => {

    $("#logoutButton").on("click", () => {
        logoutFunction();
    });

});