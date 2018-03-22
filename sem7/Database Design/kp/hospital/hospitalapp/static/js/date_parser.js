FILTERS = {
    date_from: "01.01.1970",
    date_to: "31.12.2099",
    specialization: "",
    visit_purpose: ""
};


$("#admission_date_from, #admission_date_to").on("input", function () {
   value = $(this).val().trim();
   console.log(value);
   full_date_pattern = /^\d\d([/\.-])\d\d\1\d\d\d\d$/;
   month_year_pattern = /^\d\d[/\.-]\d\d\d\d$/;
   year_pattern = /^\d\d\d\d$/;

   if ($(this).attr("id") === "admission_date_from") {
       if (full_date_pattern.test(value)) {
           $("#admissions_search_btn").attr("disabled", false);
           pattern = /(\d\d).(\d\d).(\d\d\d\d)/g;
           full_date = pattern.exec(value);
           day = full_date[1];
           month =  full_date[2];
           year = full_date[3];
           FILTERS.date_from = $.grep([day, month, year], Boolean).join(".");
       } else if (month_year_pattern.test(value)) {
           $("#admissions_search_btn").attr("disabled", false);
           full_date = pattern.exec(value);
           month =  full_date[1];
           year = full_date[2];
           day = "01";
           FILTERS.date_from = $.grep([day, month, year], Boolean).join(".");
       } else if (year_pattern.test(value)) {
           $("#admissions_search_btn").attr("disabled", false);
           year = value;
           month = "01";
           day = "01";
           FILTERS.date_from = $.grep([day, month, year], Boolean).join(".");
       } else if (value.length === 0) {
           $("#admissions_search_btn").attr("disabled", false);
           min_date = "01.01.1970";
           FILTERS.date_from = min_date;
       } else {
           $("#admissions_search_btn").attr("disabled", true);
       }
   } else {
       if (full_date_pattern.test(value)) {
           $("#admissions_search_btn").attr("disabled", false);
           pattern = /(\d\d).(\d\d).(\d\d\d\d)/g;
           full_date = pattern.exec(value);
           day = full_date[1];
           month =  full_date[2];
           year = full_date[3];
           FILTERS.date_to = $.grep([day, month, year], Boolean).join(".");
       } else if (month_year_pattern.test(value)) {
           $("#admissions_search_btn").attr("disabled", false);
           pattern = /(\d\d).(\d\d\d\d)/g;
           full_date = pattern.exec(value);
           day = "01";
           month = full_date[1];
           year = full_date[2];
           FILTERS.date_to = $.grep([day, month, year], Boolean).join(".");
       } else if (year_pattern.test(value)) {
           $("#admissions_search_btn").attr("disabled", false);
           day = "01";
           month = "01";
           year = value;
           FILTERS.date_to = $.grep([day, month, year], Boolean).join(".");
       } else if (value.length === 0) {
           $("#admissions_search_btn").attr("disabled", false);
           max_date = "31.12.2099";
           FILTERS.date_to = max_date;
       } else {
           $("#admissions_search_btn").attr("disabled", true);
       }
   }
});


/*
$(".specialization").click(function () {
    specialization = $(this).data();
    console.log(specialization)
});

$(".visit_purpose").click(function () {
    visit_purpose = $(this).data();
});
*/


$("#admissions_search_btn").click(function () {
    FILTERS.specialization = $("#specialization_select option:selected").data("specialization");
    FILTERS.visit_purpose = $("#visit_purpose_select option:selected").data("visit_purpose");
    if (FILTERS.specialization === undefined)
        FILTERS.specialization = "";
    if (FILTERS.visit_purpose === undefined)
        FILTERS.visit_purpose = "";

    $.ajax({
        url: "/doctor/issues_history/",
        type: "GET",
        data: {
            "target": "get admissions with filter",
            "date_from": FILTERS.date_from,
            "date_to": FILTERS.date_to,
            "visit_purpose": FILTERS.visit_purpose,
            "specialization": FILTERS.specialization,
        },
        success: function (admissions) {
            $("#admissions_tbody").html("");
            for (i in admissions) {
                admission_row = $("<tr role=button class='admission_info' data-admission_id="+admissions[i]["id"]+"></tr>");
                doctor_specialization = "<td>"+admissions[i]["doctor_specialization"]+"</td>";
                visit_purpose = "<td>"+admissions[i]["visit_purpose"]+"</td>";
                doctor_last_name = "<td>"+admissions[i]["doctor_last_name"]+"</td>";
                doctor_first_name = "<td>"+admissions[i]["doctor_first_name"]+"</td>";
                doctor_patronymic = "<td>"+admissions[i]["doctor_patronymic"]+"</td>";
                admission_date = "<td>"+admissions[i]["admission_date"]+"</td>";
                admission_row.append($.grep([doctor_specialization, visit_purpose,admission_date, doctor_last_name, doctor_first_name, doctor_patronymic], Boolean).join("\n"));
                $("#admissions_tbody").append(admission_row);
            }
        }
    });
});

$(document).on("click", ".admission_info", function() {
    admission_id = $(this).data("admission_id");
    target_url = "/doctor/review/"+admission_id;
    window.location.href = target_url
});