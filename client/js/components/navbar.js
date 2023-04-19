$().ready(() => {

    validSession.then(d => {
        if (d.status_code === 200) {
            $("#btn-register").hide();
            $("#btn-login").hide();
            $("#btn-logout").show();
        } else {
            $("#btn-register").show();
            $("#btn-login").show();
            $("#btn-logout").hide();
        }
    });

});