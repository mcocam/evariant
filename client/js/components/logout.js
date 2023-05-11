function logoutFunction(){

    axios
        .post('/api/users/logout')
        .then(response => {
            console.log(response)
            window.location.href = './index.html';
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