/**
 * Code Summary:
 * This code handles the visibility of registration, login, and logout buttons based on the session status.
 */

$().ready(() => {

    // Show registration and login buttons, hide logout button by default
    $("#btn-register").show();
    $("#btn-login").show();
    $("#btn-logout").hide();

    try{
        // Check if a valid session exists
        validSession
        .then(d => {
        if (d.status === 200) {
            // Valid session exists, hide registration and login buttons, show logout button
            $("#btn-register").hide();
            $("#btn-login").hide();
            $("#btn-logout").show();
        } else {
            // No valid session, show registration and login buttons, hide logout button
            $("#btn-register").show();
            $("#btn-login").show();
            $("#btn-logout").hide();
        }
    })
    .catch(e => {
        console.log(e);
        // Error occurred, show registration and login buttons, hide logout button
        $("#btn-register").show();
        $("#btn-login").show();
        $("#btn-logout").hide();
    });

    }catch(e){
        console.log(e);
    }
});