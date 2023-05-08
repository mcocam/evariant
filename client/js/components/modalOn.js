$().ready(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const modalParam = urlParams.get('modal');

    setTimeout( () => {
        if(modalParam){
            const login = $('#login');
            login.modal("show");
        }
    },100)
})