$().ready(() => {

    validSession.then(d => {
        if (d.status_code === 200) {
            // DO NOTHING
            console.log("Guard: Session ok!");
        } else {
            console.log("Guard: Session down!");
            alert("You must be logged in to view this page!");
            window.location.href = './index.html';
        }
    });

});