function validateCookie() {

    axios
        .post('/api/users/verify')
        .then(response => {
            console.log(response)
            console.log(response.data.error)
            if(!response.data.error)
            {
                
            }
        })
        .catch(e => {
            console.log(e);
            return false;
        });
};

$().ready(() => {

    // validateCookie();
});