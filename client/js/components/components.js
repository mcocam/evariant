/* 
The file contains the logic to inject components. It only works inside a server environment
In order to get it work, the script must be linked on HTML
Just the array of components must be edit
*/

// List of components to inject
const components = [
    {
        id: "#nav",
        path: "./components/navbar.html"
    },
    {
        id: "#loginModal",
        path: "./components/login.html"
    },
    {
        id: "#landing",
        path: "./components/landing.html"
    },
    {
        id: "#footer",
        path: "./components/footer.html"
    },
    {
        id: "#snpRequest",
        path: "./components/snpRequest.html"
    }
    
];

// Injector. DON'T TOUCH
const addComponents = (components) =>  components.forEach(c =>  $(c.id).load(c.path) );
$().ready( () =>  addComponents(components));