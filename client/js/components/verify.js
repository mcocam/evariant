function validateCookie() {

    axios
        .post('/api/users/verify')
        .then(response => {
            console.log(response)
            console.log(response.error)
            if(!response.error)
            {

            }
        })
        .catch(e => {
            console.log(e);
            return false;
        });
};

$().ready(() => {

    validateCookie();
});