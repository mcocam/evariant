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





    // Ejemplo de Drag and Drop
    var dropZone = document.getElementById('drag-drop-zone');
    dropZone.addEventListener('dragover', handleDragOver, false);
    dropZone.addEventListener('drop', handleFileSelect, false);

    

      
});

//leer
function leerArchivo(e) {
    var archivo = e.target.files[0];
    if (!archivo) {
      return;
    }
    var lector = new FileReader();
    lector.onload = function(e) {
      var contenido = e.target.result;
      mostrarContenido(contenido);
    };
    lector.readAsText(archivo);
  }
  
  function mostrarContenido(contenido) {
    var elemento = document.getElementById('contenido-archivo');
    elemento.innerHTML = contenido;
  }

  //

function handleFileSelect(evt) {
    evt.stopPropagation();
    evt.preventDefault();
    
    var files = evt.dataTransfer.files; // Get the file objects
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
      console.log('Se ha cargado el archivo: ' + fastaFile);
      
      //Leer el archivo
      var lector = new FileReader();
      lector.onload = function(fastaFile) {
        var contenido = fastaFile.target.result;
        mostrarContenido(contenido);
      };
      lector.readAsText(fastaFile.target.files);
    } else {
      alert('No se ha seleccionado un archivo .fasta');
    }
  }
  
  function handleDragOver(evt) {
    evt.stopPropagation();
    evt.preventDefault();
    evt.dataTransfer.dropEffect = 'copy';
  }
