$().ready(() => {

    // Event listener for the click event on the element with id "landing_register"
    $("#landing_register").on("click", () => { 
        // Redirects the user to the "register.html" page
        window.location.href = "./register.html";
    });
});