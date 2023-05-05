/**
 * @file This file contains functions to send a file to the server and style the process
 * @autora Ani Valle
 */

$().ready(() => { 

    // Clicking on the "next" button of step 1 hides it and shows step 2.
    // show step 2 and hide step 1
    $("#btn_next_step1").on("click", () => { 
        $("#snp_step2").show();
        $("#snp_step1").hide();        
    });

    // show step 1 and hide step 2
    $("#btn_back_step2").on("click", () => {
        $("#snp_step1").show();
        $("#snp_step2").hide();
    });

    // Show progress bar
    $("#btn_next_step2").on("click", () => { 
        $("#div_progress").show();
    });

    // Hide the progress bar
    $("#btn_progress").on("click", () => {
        $("#div_progress").hide();
    });

    
    /**-------------------- DRAG AND DROP ---------------------------- */

    // Collect item
    var dropZone = document.getElementById('drag-drop-zone');
    var fileInput = document.getElementById('file-input');

    // When dragging a file add the active class
    dropZone.addEventListener('dragover', handleDragOver, false);
    $(dropZone).on("dragover", function(event) {
      event.preventDefault();
      $(this).addClass("active");
    });

    // When a file is dropped remove the active class
    dropZone.addEventListener('drop', handleFileSelect, false);
    $(dropZone).on("drop", function(event) {
      event.preventDefault();
      $(this).removeClass("active");
    });

    // Action on click
    dropZone.addEventListener('click', function() {
      fileInput.click();
    });
    fileInput.addEventListener('change', handleFileSelect, false);


    /**-------------------- PROGRESS BAR ---------------------------- */
    // Ejemplo de actualizar el progress bar
    const progressBar = document.getElementById('progress-bar');
    const progressValue = document.getElementById('progress-value');

    function actualizarBarraDeProgreso(valor) {
        progressBar.value = valor;
        progressValue.textContent = valor;
    }
    // Ejemplo de uso
    actualizarBarraDeProgreso(50);
    
});

/**-------------------- FUNCTION OF DRAG AND DROP ---------------------------- */

// FUNCION ENVIAR ARCHIVO
const sendFile = (file, request_title) =>{
  
  const body = new FormData();
  body.append("file",file, request_title);
  //body.append("title", request_title);

  fetch("api/files/add_fasta", {
      method: "POST",
      body: body,
      headers: {
          "Access-Control-Allow-Origin": "*"
      }
  })
  .then(response => response.json())
  .then(data => {
    //console.log(data);
    message = data.message;
    //Display a message to the user
    switch (message) {
      case "911":
        $("#msgRequest").html('<p class="text-center fs-6 fw-bold text-danger">.FASTA file Incorrect</p>');
        break;
      case "912":
        $("#msgRequest").html('<p class="text-center fs-6 fw-bold text-success"> Successfully Processed </p>');
        break;
      case "913":
        $("#msgRequest").html('<p class="text-center fs-6 fw-bold text-warning"> Served has failed, try later </p>');
        break;
    }
  })
  .catch(error => console.error(error));
}


//----------------------------------------------------------------
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

//----------------------------------------------------------------
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
    // Get request title
    var request_title = $("#request_title").val();
    // Send the file to the server
    sendFile(fastaFile, request_title);

  } else {
  // Otherwise an alert will be displayed.
    alert('The file you have selected is not allowed. \nSelect a .fasta file');
  }
}

//----------------------------------------------------------------
function validateRequestTitle() {
  // Collect Valued email
  request_title = $("#request_title").val();

  // Regext Validate Title
  var regex = new RegExp(/^(?=.*[a-zA-Z0-9()>< ])[a-zA-Z0-9()>< ]{5,30}$/);
  if (regex.test(request_title)) {
    $("#msgTitle").html("");
    return true; // No hay errores
  }else{
    $("#msgTitle").html("<p>The title must have at least 5 characters and a maximum of 30. \nParentheses and symbols greater than and less than are allowed..</p>");
  }
}

// ACTIVATE BUTTON 1
["#request_title"].forEach((i) => { 
  $(i).on("change", () => {
    handleTitleButton()
  })
})
const handleTitleButton = () => {
  let state = [];

  ["#request_title"].forEach((input, index) => {
    const value = $(input).val();
      let isOK = false;

      if(index === 0){
        isOK = validateRequestTitle();
      }
    state.push(isOK);
  });

  if(state.some(data => data === false)){
    //Desactivar
    $('#btn_next_step1').prop('disabled', true);
  }else{
    //Activar
    $('#btn_next_step1').prop('disabled', false);
  }
}

//----------------------------------------------------------------

