$().ready(() => {

    $("#btn-register").show();
    $("#btn-login").show();
    $("#btn-myProfile").hide();
    $("#btn-logout").hide();

    try{
        validSession
        .then(d => {
        if (d.status === 200) {
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
    })
    .catch(e => {
        console.log(e);
        $("#btn-register").show();
        $("#btn-login").show();
        $("#btn-myProfile").hide();
        $("#btn-logout").hide();
    });

    }catch(e){
        console.log(e);
    }



});