validSession
    .then(d => {
    console.log(d);
    if (d.status === 200) {
        // DO NOTHING
        console.log("Guard: Session ok!");
    } else {
        console.log("Guard: Session down!");
        window.location.href = './index.html?modal=true';
    }
    })
    .catch(e => {
        window.location.href = './index.html?modal=true';
    });