$().ready(() => {
    // Get the URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    // Get the value of the 'modal' parameter
    const modalParam = urlParams.get('modal');

    // Delay the execution to ensure the DOM is ready
    setTimeout( () => {
        // Check if the 'modal' parameter exists
        if(modalParam){
            // Show the login modal
            const login = $('#login');
            login.modal("show");
        }
    },100)
})