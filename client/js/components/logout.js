/**
 * Function to perform user logout.
 */
function logoutFunction(){
    // Send a POST request to the server for user logout
    axios
        .post('/api/users/logout')
        .then(response => {
            // Redirect the user to the index.html page
            window.location.href = './index.html';
        })
        .catch(e => {
            console.log(e);
            return false;
        });
};

/**
 * Perform the necessary actions when the document is ready.
 */
$().ready(() => {

    // Event listener for the logout button click.
    $("#logoutButton").on("click", () => {
        // Call the logoutFunction to initiate the logout process
        logoutFunction();
    });

});