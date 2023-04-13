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

      
});
