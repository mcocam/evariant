$().ready(() => {

    validSession.then(d => {
        if (d.status_code === 200) {
            $("#btn-register").hide();
            $("#btn-login").hide();
            $("#btn-myProfile").show();
            $("#btn-logout").show();
        } else {
            $("#btn-register").show();
            $("#btn-login").show();
            $("#btn-myProfile").hide();
            $("#btn-logout").hide();
        }
    });

});