$().ready(() => {

    validSession.then(d => {
        if (d.status_code === 200) {
            // DO NOTHING
            console.log("Guard: Session ok!");
        } else {
            console.log("Guard: Session down!");
            window.location.href = './index.html';
        }
    });

});