$().ready(() => {

    $("#btn-register").show();
    $("#btn-login").show();
    $("#btn-logout").hide();

    try{
        validSession
        .then(d => {
        if (d.status === 200) {
            $("#btn-register").hide();
            $("#btn-login").hide();
            $("#btn-logout").show();
        } else {
            $("#btn-register").show();
            $("#btn-login").show();
            $("#btn-logout").hide();
        }
    })
    .catch(e => {
        console.log(e);
        $("#btn-register").show();
        $("#btn-login").show();
        $("#btn-logout").hide();
    });

    }catch(e){
        console.log(e);
    }



});