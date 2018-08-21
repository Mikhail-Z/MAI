SELECTED_ELEMENTS = {
    "visit_purpose": false,
    "admission_type": false,
    "med_polise_type": false,
    "patient_is_right": false
};

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


function make_input_disabled(element) {
    element.attr("disabled", true);
    element.val("");
}

$("#medical_police_type").change(function () {
   med_police_type_id = $("#medical_police_type option:selected").attr("id");
   med_police_series = $("#med_police_series");
   med_police_number = $("#med_police_number");
   if (med_police_type_id === "no_med_police_type") {
        SELECTED_ELEMENTS.med_polise_type = false;
        make_input_disabled(med_police_number);
        make_input_disabled(med_police_series);
   } else if (med_police_type_id === "old_med_police_type") {
        SELECTED_ELEMENTS.med_polise_type = true;
        med_police_number.attr("disabled", false);
        med_police_series.attr("disabled", false);
   } else if (med_police_type_id === "new_med_police_type") {
        SELECTED_ELEMENTS.med_polise_type = true;
        med_police_number.attr("disabled", false);
        make_input_disabled(med_police_series);
   }
});

$("#med_police_series, #med_police_number").on("input", function () {
    med_police_series = $("#med_police_series");
    med_police_number = $("#med_police_number");
    if (med_police_series.prop("disabled") === false) {
        console.log(74);
        if (med_police_series.val().length === 11 && med_police_number.val().length === 16)
            $("#patient_search_btn").attr("disabled", false);
        else
            $("#patient_search_btn").attr("disabled", true);
    } else {
        if (med_police_number.val().length === 16)
            $("#patient_search_btn").attr("disabled", false);
        else
            $("#patient_search_btn").attr("disabled", true);
    }


});

$("#patient_search_btn").click(function () {
    med_police_type_id = $("#medical_police_type option:selected").data()["med_police_type_id"];
    police_series = $("#med_police_series").val();
    police_number = $("#med_police_number").val();

    patient_search_table = $("#patient_search_table");
    patient_search_table.find("tbody").html("");
    $("#patient_not_found_msg").remove();
    $.ajax({
        url: "/doctor/review/patient_search/",
        type: "GET",
        data: {
            "police_type": med_police_type_id,
            "police_series": police_series,
            "police_number": police_number
        },
        success: function (patient_info) {
            if (patient_info.length === 0) {
                elem = "<b id='patient_not_found_msg'>Пациент не найден.</b>"
                patient_search_table.after(elem)
            } else {
                for (i in patient_info) {
                    console.log(patient_info[i]["last_name"], patient_info[i]);
                    last_name = "<td>" + patient_info[i]["last_name"] + "</td>";
                    first_name = "<td>" + patient_info[i]["first_name"] + "</td>";
                    patronymic = "<td>" + patient_info[i]["patronymic"] + "</td>";
                    birthday = "<td>" + patient_info[i]["date_birth"] + "</td>";
                    all_right = "<td><input data-patient="+patient_info[i]["id"]+" "+"class='right_patient_chbx' type='checkbox'></td>";
                    search_row = $("<tr></tr>");
                    col_values = $.grep([last_name, first_name, patronymic, birthday, all_right], Boolean).join("\n")
                    search_row.html(col_values);
                    patient_search_table.find("tbody").append(search_row)
                }
            }
        }
    })
});


function make_form_active(form) {
    form.css("opacity", 1.0);
    form.find("input[type=submit]").attr("disabled", false);
}

function make_form_disabled(form) {
    form.css("opacity", 0.5);
    form.find("input[type=submit]").attr("disabled", true);
}

$(document).on("change", ".right_patient_chbx", function () {
    is_checked = $(this).prop("checked");
    form = $("form");
    patient_id = $(this).data("patient");
    if (is_checked) {
        make_form_active(form);
        $.ajax({
            url: "/doctor/review/",
            type: "GET",
            data: {
                "cur_reviewed_patient_id": patient_id
            },
            success: function (resp) {
                first_stage_specializations = resp["first_stage_specializations"];
                first_stage_procedures = resp["first_stage_procedures"];
                first_stage_specializations_elem = $("#first_stage_specializations");
                first_stage_procedures_elem = $("#first_stage_procedures");
                console.log(first_stage_specializations);
                for (i = 0; i < first_stage_specializations.length - 1; i++) {
                    specialization = first_stage_specializations[i]["specialization__specialization_name"];
                    console.log(specialization);
                    specialization_elem = $("<span class='choose_several_states' role='button'>" + specialization + ", " + "</span> ");
                    first_stage_specializations_elem.prepend(specialization_elem);
                }
                specialization = first_stage_specializations[first_stage_specializations.length - 1]["specialization__specialization_name"];
                specialization_elem = $("<span class='choose_several_states' role='button'>" + specialization + "</span> ");
                first_stage_specializations_elem.prepend(specialization_elem);

                for (i = 0; i < first_stage_procedures.length - 1; i++) {
                    procedure = first_stage_procedures[i]["name"];
                    console.log(procedure);
                    procedure_elem = $("<span class='choose_several_states' role='button'>" + procedure + ", " + "</span> ");
                    first_stage_procedures_elem.prepend(procedure_elem);
                }
                procedure = first_stage_procedures[first_stage_procedures.length - 1]["name"];
                procedure_elem = $("<span class='choose_several_states' role='button'>" + procedure + "</span> ");
                first_stage_procedures_elem.prepend(procedure_elem);

                second_stage_specializations = resp["second_stage_specializations"];
                second_stage_procedures = resp["second_stage_procedures"];
                second_stage_specializations_elem = $("#second_stage_specializations");
                second_stage_procedures_elem = $("#second_stage_procedures");

                for (i = 0; i < second_stage_specializations.length - 1; i++) {
                    specialization = second_stage_specializations[i]["specialization__specialization_name"];
                    console.log(specialization);
                    specialization_elem = $("<span class='choose_several_states' role='button'>" + specialization + ", " + "</span> ");
                    second_stage_specializations_elem.prepend(specialization_elem);
                }
                specialization = second_stage_specializations[second_stage_specializations.length - 1]["specialization__specialization_name"];
                specialization_elem = $("<span class='choose_several_states' role='button'>" + specialization + "</span> ");
                second_stage_specializations_elem.prepend(specialization_elem);

                for (i = 0; i < second_stage_procedures.length - 1; i++) {
                    procedure = second_stage_procedures[i]["name"];
                    console.log(procedure);
                    procedure_elem = $("<span class='choose_several_states' role='button'>" + procedure + ", " + "</span> ");
                    second_stage_procedures_elem.prepend(procedure_elem);
                }
                procedure = second_stage_procedures[second_stage_procedures.length - 1]["name"];
                procedure_elem = $("<span class='choose_several_states' role='button'>" + procedure + "</span> ");
                second_stage_procedures_elem.prepend(procedure_elem);

            }
        })
    } else {
        make_form_disabled(form);
    }
});

function hideSpecificInputs(selector) {
    selector.css("display", "none");
    selector.find("input").attr("disabled", true);
    selector.find("textarea").attr("disabled", true);
}

function showSpecificInputs(selector) {
    selector.css("display", "inline");
    selector.find("input").attr("disabled", false);
    selector.find("textarea").attr("disabled", false);
}

$("#visit_purpose").on("change", function () {
    dispanserization_only_blocks = $(".dispanserization_only");
    review_only_blocks = $(".review_only");
    if ($("#visit_purpose option:selected").text() === "Диспансеризация") {
        hideSpecificInputs(review_only_blocks);
        showSpecificInputs(dispanserization_only_blocks);
    } else {
        hideSpecificInputs(dispanserization_only_blocks);
        showSpecificInputs(review_only_blocks);
    }
});


$("#ticket_number").on("input", function () {
    var ticket_number_len = 6;
    if ($("#ticket_number").val().length === ticket_number_len) {
        $("#patient_search_by_ticket_btn").attr("disabled", false);
    }
});

function showSpecializationsAndProcedures() {
    $("")
}

$("#patient_search_by_ticket_btn").click(function () {
    ticket_number = $("#ticket_number").val();

    patient_search_table = $("#patient_search_table");
    patient_search_table.find("tbody").html("");
    $("#patient_not_found_msg").remove();
    $.ajax({
        url: "/doctor/review/patient_search/",
        type: "GET",
        data: {
            "ticket_number": ticket_number
        },
        success: function (patient_info) {
            if (patient_info.length === 0) {
                elem = "<b id='patient_not_found_msg'>Пациент не найден.</b>"
                patient_search_table.after(elem)
            } else {
                for (i in patient_info) {
                    last_name = "<td>" + patient_info[i]["last_name"] + "</td>";
                    first_name = "<td>" + patient_info[i]["first_name"] + "</td>";
                    patronymic = "<td>" + patient_info[i]["patronymic"] + "</td>";
                    birthday = "<td>" + patient_info[i]["date_birth"] + "</td>";
                    all_right = "<td><input data-patient="+patient_info[i]["id"]+" "+"class='right_patient_chbx' type='checkbox'></td>";
                    search_row = $("<tr></tr>");
                    col_values = $.grep([last_name, first_name, patronymic, birthday, all_right], Boolean).join("\n")
                    search_row.html(col_values);
                    patient_search_table.find("tbody").append(search_row)
                }
            }
        }
    })
});