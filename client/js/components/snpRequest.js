//

$().ready(() => { 

    // Clicking on the "next" button of step 1 hides it and shows step 2.
    $("#btn_next_step1").on("click", () => { 
        $("#snp_step2").show();
        $("#snp_step1").hide();

    });

    $("#btn_back_step2").on("click", () => {
        $("#snp_step1").show();
        $("#snp_step2").hide();
    });
});

