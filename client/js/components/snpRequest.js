//

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

    // Ejemplo de actualizar el progress bar
    const progressBar = document.getElementById('progress-bar');
    const progressValue = document.getElementById('progress-value');

    function actualizarBarraDeProgreso(valor) {
        progressBar.value = valor;
        progressValue.textContent = valor;
    }
    // Ejemplo de uso
    actualizarBarraDeProgreso(50);


    
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

    
});

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
  
  if (fastaFile) {
    // Do something with the fasta file
    alert('Se ha cargado el archivo: ' + fastaFile.name);
    console.log('Se ha cargado el archivo: ' + fastaFile.name);

  } else {
    alert('No se ha seleccionado un archivo .fasta');
  }
}



/** Function upload Fasta */
function uploadFasta(body){

    axios
      .post('/api/files/add_fasta', body)
      .then(response)
}


