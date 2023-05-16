/**
 * Code Summary:
 * This code validates the user's session by sending a request to the server. If the session is valid (status 200),
 * it logs a success message. If the session is invalid or an error occurs, it redirects the user to the index.html page
 * with the modal=true parameter.
 */

// Perform session validation
validSession
    .then(d => {
    console.log(d);
    if (d.status === 200) {
        // Session is valid, do nothing
        console.log("Guard: Session ok!");
    } else {
        // Session is invalid, redirect to index.html with modal=true
        console.log("Guard: Session down!");
        window.location.href = './index.html?modal=true';
    }
    })
    .catch(e => {
        // An error occurred, redirect to index.html with modal=true
        window.location.href = './index.html?modal=true';
    });