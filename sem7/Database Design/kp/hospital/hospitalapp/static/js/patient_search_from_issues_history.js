$("#full_name_input").on("input", function () {
    cur_text = $(this).val();
    patient_search_table = $("#patient_search_table");
    patient_search_table.find("tbody").html("");
    $("#patient_not_found_msg").remove();
    if (cur_text.length >= 3) {
        $.ajax({
            url: "/doctor/issues_history/",
            type: "GET",
            data: {
                "full_name": cur_text
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
                        medical_police_number = "<td>" + patient_info[i]["medical_police_number"] + "</td>";
                        search_row ="<tr data-patient="+patient_info[i]['id']+" role='button' class='patient_search'></tr>";
                        search_row = $(search_row);

                        col_values = $.grep([last_name, first_name, patronymic, birthday, medical_police_number], Boolean).join("\n")
                        search_row.html(col_values);
                        patient_search_table.find("tbody").append(search_row);
                    }
                }
            }
        })
    }
});

$(document).on("click", ".patient_search", function () {
    table_row = $(this);
    patient_id = table_row.data("patient");

    $.ajax({
        url: "/doctor/issues_history/",
        type: "GET",
        data: {
            "patient_id": patient_id
        },
        success: function (admissions) {
            table_row.attr("class", "alert alert-success");
            console.log(admissions.length);
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
    })
});