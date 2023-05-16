/**
 * Code Summary:
 * This file contains functions to send a file to the server and style the process
 */

//----------------------------------------------------------------
$().ready(() => {
    // Clicking on the "next" button of step 1 hides it and shows step 2.
    // show step 2 and hide step 1
    $("#btn_step1").on("click", () => { 
        $("#phylo_step2").show();
        $("#phylo_step1").hide();        
    });

    // show step 1 and hide step 2
    $("#btn_back_phylo").on("click", () => {
        $("#phylo_step1").show();
        $("#phylo_step2").hide();
    });

    /**-------------------- DRAG AND DROP ---------------------------- */

    // Collect item
    var dropZone = document.getElementById('phylo_drag-drop-zone');
    var fileInput = document.getElementById('phylo-file');

    // When dragging a file add the active class
    dropZone.addEventListener('dragover', handleDragOver, false);
    $(dropZone).on("dragover", function(event) {
      event.preventDefault();
      $(this).addClass("active");
      $("#msgRequestPhylo").html('<p></p>');
    });

    // When a file is dropped remove the active class
    dropZone.addEventListener('drop', handleFileSelect, false);
    $(dropZone).on("drop", function(event) {
      event.preventDefault();
      $(this).removeClass("active");
      $("#msgRequestPhylo").html('<p></p>');

    });

    // Action on click
    dropZone.addEventListener('click', function() {
      fileInput.click();
      $("#msgRequestPhylo").html('<p></p>');

    });
    fileInput.addEventListener('change', handleFileSelect, false);

});

/**-------------------- VALIDATE TITLE ---------------------------- */
/**
 * Validate the title of the Request
 * If it does not meet the specifications, it shows a message to the user
 */
function validateRequestTitle() {
    // Collect Valued email
    phylo_title = $("#phylo_title").val();
  
    // Regext Validate Title
    var regex = new RegExp(/^(?=.*[a-zA-Z0-9()>< ])[a-zA-Z0-9()><\- ]{5,30}$/);
    if (regex.test(phylo_title)) {
      $("#pMsgTitle").html("");
      return true; // No errors
    }else{
      $("#pMsgTitle").html("<p>The title must have at least 5 characters and a maximum of 30. \nParentheses and symbols greater than and less than are allowed..</p>");
    }
  }

/**-------------------- ACTIVATE BUTTON STEP1 ---------------------------- */
/**
 * Validates the input of the title for each change that there is and
 *  activates or deactivates the button in question of the validation.
 */
["#phylo_title"].forEach((i) => { 
    $(i).on("change", () => {
      handleTitleButton()
    })
})

// Function to handle the state of the sign-in button
const handleTitleButton = () => {
  let state = [];

  // Validate title inputs
  ["#phylo_title"].forEach((input, index) => {
    const value = $(input).val();
      let isOK = false;
      if(index === 0){
        isOK = validateRequestTitle();
      }
    state.push(isOK);
  });

  if(state.some(data => data === false)){
    // Disable the sign-in button
    $('#btn_step1').prop('disabled', true);
  }else{
    // Enable the sign-in button
    $('#btn_step1').prop('disabled', false);
  }
}

/**-------------------- ENVIAR ARCHIVO ---------------------------- */
/**
 * Receive the title and file to send to the server.
 * It then retrieves the response and displays messages to the user depending on. 
 * @param {*} file 
 * @param {*} phylo_title
 */
const sendFile = (file, phylo_title) =>{
  
    // Create a FormData object and add the file and request title to the request body.
    const body = new FormData();
    body.append("file",file, phylo_title);
  
    // Make a fetch request to the api/files/add_fasta endpoint with the POST method, request body, and request headers.
    fetch("api/phylo/add_multi_fasta", {
        method: "POST",
        body: body,
        timeout: 0,
        headers: {
            "Access-Control-Allow-Origin": "*"
        }
    })
    .then(response => response.json())
    .then(data => {

      $("#phylo_spinner").hide();
      $("#phylo_spinner_text").hide();
      $('#btn_back_phylo').prop('disabled', false);

      console.log(data.message);
      // Parse the response as a JSON object.
      // Check the message returned by the server and display a corresponding message to the user.
      switch (data.message) {
        case "925":
          // Display an error message if the .fasta file is incorrect.
          $("#msgRequestPhylo").html('<p class="text-center fs-6 fw-bold text-danger"> Incorrect Multifasta file. </p>');

          break;
        case "900":
          // Display a success message if the .fasta file was processed successfully.
          $("#msgRequestPhylo").html('<p class="text-center fs-6 fw-bold text-success"> Successfully Processed </p>');

          // Activate the snp_done button.
          $('#phylo_done').prop('disabled', false);

          setTimeout(() => {
            location.reload();
          }, 500)

          break;
        case "927":
          // Display a warning message if the server failed.
          $("#msgRequestPhylo").html('<p class="text-center fs-6 fw-bold text-warning"> Served has failed, try later </p>');

          break;
        default:
          $("#msgRequestPhylo").html('<p></p>');

      }
    })
    .catch(error => {
      $("#phylo_spinner").hide();
      $("#phylo_spinner_text").hide();
      console.log(error);
      $("#msgRequestPhylo").html('<p class="text-danger text-center">Something gone wrong!</p>');

    });
}

/**-------------------- FUNCTION OF DRAG AND DROP ---------------------------- */
/**
 * Function handleDragOver
 * Handle the drag action
 * @param {Event} evt 
 * @author Ani Valle
 */
function handleDragOver(evt) {
    evt.stopPropagation();
    evt.preventDefault();
    evt.dataTransfer.dropEffect = 'copy';
}

/**
 * Function handleFileSelect
 * It handles the selected file
 * The stopPropagation() and preventDefault() methods are to prevent 
 *  the browser from handling the drag and drop event by default.
 * Check if the selected file is a .fasta file.
 * @param {Event} evt
 * @author Ani Valle
 */
function handleFileSelect(evt) {
    evt.stopPropagation();
    evt.preventDefault();
  
    var files = evt.target.files || evt.dataTransfer.files; // Get the file objects
    var fastaFile = null;
    
    for (var i = 0, f; f = files[i]; i++) {
      // Only accept .fasta files
      if (f.name.split('.').pop() !== 'fasta') {
        continue;
      }
      fastaFile = f;
      break;
    }
    // If it is a .fasta file it will be sent to the server
    if (fastaFile) {

      $('#btn_back_phylo').prop('disabled', true);
      // Show spinner and text
      $("#phylo_spinner").show();
      $("#phylo_spinner_text").show();
      
      // Get request title
      var phylo_title = $("#phylo_title").val();
      // Send the file to the server
      sendFile(fastaFile, phylo_title);
  
    } else {
    // Otherwise an alert will be displayed.
      alert('The file you have selected is not allowed. \nSelect a .fasta file');
    }
}