var CURRENT_SPECIALIZATION_ID;
var CURRENT_DOCTOR_ID;
var CURRENT_APPOINTMENT_DATE;
var CURRENT_APPOINTMENT_ID;

var CURRENT_APPOINTMENT_ID;
var NUMBER_OF_CHOSEN_ELEMENTS;

var APPOINTMENT_TIME_WAS_CHOSEN = false;
var SPECIALIZATION_WAS_CHOSEN = false;
var DOCTOR_WAS_CHOSEN = false;

function div(val, by){
    return (val - val % by) / by;
}

function insertAfter(newNode, referenceNode) {
  referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

function deleteAppointmentDateFromPage() {

    appointment_dates = document.getElementById("appointment_dates_list");
    appointment_dates.innerHTML = "";
}

function deleteDoctorsFromPage() {
    doctors_list = $("#doctors_list");
    doctors_list.children().remove();
}

function deleteAppointmentTimeFromPage() {
    appointment_times = document.getElementsByClassName("time_appointment")[0];
    appointment_times.innerHTML = "";
}

function setSubmitBtnActive() {
    btn = document.getElementById('submit_btn');
    btn.className = "btn btn-primary btn-lg active";
}

function setSubmitBtnDisabled() {
    btn = document.getElementById('submit_btn');
    btn.className = "btn btn-primary btn-lg disabled";
}


$(document).ready(function () {
    if ($(this).width() < 1000) {
        datetime_appointment_header = $("#datetime_appointment_header").remove();
        datetime_appointment = $(".datetime_appointment").remove();

        go2appointment_datetime = $("<a href='#down'><button style='vertical-align: middle' class='btn btn-default btn-lg' doctor_id='go2appointment_datetime_btn'>Далее</button></a>");
        $(".bodies").append(go2appointment_datetime);

        moved_header = $("<a name='down' style='color: black;'><div class='search_row' style='margin-top: 60%%' doctor_id='moved_header'></div></a>");
        moved_header.append(datetime_appointment_header);

        moved_body = $("<div class='moved_body'></div>");
        moved_body.append(datetime_appointment);

        $("#main").append(moved_header);
        $("#main").append(moved_body);

        $("#submit_btn").attr("style", "margin-bottom: 50%");

        go_back_btn = $("<a href='#top'><button style='margin-left: 30px; vertical-align: middle' class='btn btn-default btn-lg' doctor_id='go2appointment_datetime_btn'>Назад</button></a>");
        $(".moved_body").append(go_back_btn);
    }
});


$("#specializations_list").children().click(function (event) {
    if (CURRENT_APPOINTMENT_ID !== null)
        setSubmitBtnDisabled();
    if (CURRENT_APPOINTMENT_DATE !== null)
        deleteAppointmentTimeFromPage();
    if (CURRENT_DOCTOR_ID !== null) {
        deleteAppointmentDateFromPage();
    }
    if (CURRENT_SPECIALIZATION_ID !== null)
        deleteDoctorsFromPage();
    n = "specialization".length;
    CURRENT_SPECIALIZATION_ID = $(this).attr("id").slice(n);
    $.ajax({
        type: "GET",
        url: "/patient/appointment/",
        data: {
            specialization: CURRENT_SPECIALIZATION_ID
        },
        success: function (doctors) {
            for (var i in doctors) {
                surname = doctors[i]["doctor__last_name"];
                name_and_patronymic = $.grep([doctors[i]["doctor__first_name"], doctors[i]['doctor__patronymic']], Boolean).join(" ");
                doctor_id = "doctor" + doctors[i]["doctor__id"];

                table_row = $("<tr><td><h4>"+surname+"<br/>"+name_and_patronymic+"</h4></td></tr>");
                table_row.attr("id", doctor_id);
                $("#doctors_list").append(table_row)
            }
        }
    })
});


$("#doctors_list").click(function (event) { //почему-то не реагирует на children()
    if (CURRENT_APPOINTMENT_ID !== null)
        setSubmitBtnDisabled();
    if (CURRENT_APPOINTMENT_DATE !== null)
        deleteAppointmentTimeFromPage();
    if (CURRENT_DOCTOR_ID !== null) {
        deleteAppointmentDateFromPage();
    }
    n = "doctor".length;
    CURRENT_DOCTOR_ID = $(event.target).closest("tr").attr("id").slice(n);
    console.log(CURRENT_DOCTOR_ID);
    $.ajax({
        type: "GET",
        url: "/patient/appointment/",
        data: {
            doctor: CURRENT_DOCTOR_ID
        },
        success: function (dates_and_weekdays) {
            for (i in dates_and_weekdays) {
                innerText = $.grep([dates_and_weekdays[i]["date"], dates_and_weekdays[i]["weekday"]], Boolean).join(", ");
                table_row = $("<tr class='doctor-spec-search_row'><td><h4><b>"+innerText+"</b></h4></td></tr>");
                $("#appointment_dates_list").append(table_row);
            }
        }
    });
});

$("#appointment_dates_list").click(function (event) {
    if (CURRENT_APPOINTMENT_ID !== null)
        setSubmitBtnDisabled();
    if (CURRENT_APPOINTMENT_DATE !== null)
        deleteAppointmentTimeFromPage();
    date_and_weekday = $(event.target).text();
    CURRENT_APPOINTMENT_DATE = date_and_weekday.split(", ")[0];
    $.ajax({
        type: "GET",
        url: "/patient/appointment/",
        data: {
            date: CURRENT_APPOINTMENT_DATE
        },
        success: function (appointments_info) {
            console.log(appointments_info);
            n = appointments_info.length;
            buttonsInRowCount = 4;
            for (i = 0; i < div(n, buttonsInRowCount); i++) {
                buttonGroup = $("<div class='btn-group-lg' style='margin-bottom: 5px'></div>");
                for (j = 0; j < buttonsInRowCount; j++) {
                    idx = i*buttonsInRowCount+j;
                    if (appointments_info[idx]["free"] === true)
                        emptyButton = $("<button class='btn btn-info'></button>");
                    else
                        emptyButton = $("<button class='btn disabled'></button>");
                    emptyButton.attr("id", appointments_info[idx]["id"]);
                    emptyButton.text(appointments_info[idx]["time"]);
                    buttonGroup.append(emptyButton)
                }
                $(".time_appointment").append(buttonGroup);
            }
            buttonGroup = $("<div class='btn-group-lg' style='margin-bottom: 5px'></div>");
            for (j = 0; j < n % 4; j++) {
                console.log(i);
                idx = div(n, buttonsInRowCount) + j;
                if (appointments_info[idx]["free"] === true)
                    emptyButton = $("<button class='btn btn-info time-btn'></button>");
                else
                    emptyButton = $("<button class='btn disabled time-btn'></button>");
                emptyButton.attr("id", appointments_info[idx]["id"]);
                emptyButton.text(appointments_info[idx]["time"]);
                buttonGroup.append(emptyButton)
            }
            if (buttonGroup.length)
                $(".time_appointment").append(buttonGroup);
        }
    })
});

$(".time_appointment").on("click", "button", function () {
    if (CURRENT_APPOINTMENT_ID !== null) {
        setSubmitBtnDisabled();
    }
    CURRENT_APPOINTMENT_ID = $(this).attr("id");
    setSubmitBtnActive();
});


$("#submit_btn").click(function () {
    $("input[name='appointment_id']").val(CURRENT_APPOINTMENT_ID);
});