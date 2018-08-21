$("#icd10_input").on("input", function () {
   if ($(this).val().length >= 3) {
       $("#icd10_search_results").css("display", "inline-block");
       $.ajax({
           url: "/doctor/review/",
           type: "GET",
           data: {
               "icd10_text": $(this).val()
           },
           success: function (patients) {
               $("#icd10_search_results").html("");
               console.log(patients.length)
               for (i in patients) {
                   code = patients[i][1];
                   name = patients[i][2];
                   search_row = "<span data-icd10_id=" + patients[i][0] + " " + "role='button' class='icd10_search_row'><li onmouseover="+"this.style.backgroundColor='lightgrey'" + " " + "onmouseout="+"this.style.backgroundColor='white'"+">" +
                       "<b>" + code + "</b>" + " " + name + "</li></span>";
                   $("#icd10_search_results").append(search_row);
               }
           }
       });
   } else
       $("#icd10_search_results").css("display", "none");

});


$(document).on("click", function (event) {
    if ($(event.target).closest($(".icd10_search_row")).length) {
        icd10_id = $(event.target).closest($(".icd10_search_row")).data()["icd10_id"];
        $("input[name=icd10_id]").val(icd10_id);
        jsonInputData["icd10_id"].input = icd10_id;
        console.log($(event.target).closest($(".icd10_search_row")));
        $("#icd10_input").val($(event.target).closest($(".icd10_search_row")).text())
    }
    $("#icd10_search_results").css("display", "none");
});