var CURRENT_DOCTOR_SPECIALIZATION;
var CURRENT_APPOINTMENT_TIME;
var CURRENT_APPOINTMENT_ID;
var CURRENT_DOCTOR_ID;
var NUMBER_OF_CHOSEN_ELEMENTS;

var APPOINTMENT_TIME_WAS_CHOSEN = false;
var SPECIALIZATION_WAS_CHOSEN = false;
var DOCTOR_WAS_CHOSEN = false;

function insertAfter(newNode, referenceNode) {
  referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

function deleteAppointmentDateFromPage() {

    appointment_dates = document.getElementById("appointment_dates_list");
    appointment_dates.innerHTML = "";
}

function deleteDoctorsFromPage() {
    console.log("in delete doctors from page");
    doctors_list = $("#doctors_list");
    doctors_list.children().remove();
}

function deleteAppointmentTimeFromPage() {
    appointment_times = document.getElementsByClassName("time_appointment");
    appointment_times.innerHTML = "";
}

$("#specialization_col").on('click', 'button', function(e) {
    e.preventDefault();

    if (SPECIALIZATION_WAS_CHOSEN) {
        deleteAppointmentTimeFromPage();
        if (APPOINTMENT_TIME_WAS_CHOSEN) {
            deleteDoctorsFromPage();
            CURRENT_APPOINTMENT_ID = null;
            DOCTOR_WAS_CHOSEN = false;
        }
        CURRENT_APPOINTMENT_TIME = null;
        APPOINTMENT_TIME_WAS_CHOSEN = false;
    }

    SPECIALIZATION_WAS_CHOSEN = true;
    CURRENT_DOCTOR_SPECIALIZATION = $(this).val();
    $.ajax({
        type: "GET",
        url: "/show_appointment_time/",
        data: {
            specialization_id: $(this).val()
        },
        success: function (result) {
            for (var i in result) {
                newButton = document.createElement("button");
                newButton.className = "btn btn-default";
                newButton.innerText = result[i].appointment_time;
                newButton.value = result[i].appointment_time;
                document.getElementById('appointment_date').appendChild(newButton)
            }
        },
        error: function (result) {
            alert('error');
        }
    });
});


$('#appointment_date').on('click', 'button', function (e) {
    if (APPOINTMENT_TIME_WAS_CHOSEN) {
        deleteDoctorsFromPage();
        CURRENT_APPOINTMENT_ID = null;
        DOCTOR_WAS_CHOSEN = false;
    }

    CURRENT_APPOINTMENT_TIME= $(this).val();
    APPOINTMENT_TIME_WAS_CHOSEN = true;
    $.ajax({
            type: "GET",
            url: "/show_doctors/",
            data: {
                specialization_id:CURRENT_DOCTOR_SPECIALIZATION,
                appointment_time: $(this).val(), // < note use of 'this' here
            },
            success: function (result) {
                for (var i in result) {
                    newButton = document.createElement("button");
                    newButton.className = "btn btn-default";
                    newButton.innerText = result[i].last_name+" "+result[i].first_name+" "+result[i].patronymic;
                    newButton.value = result[i].doctor_id;
                    document.getElementById('doctor_choosing_col').appendChild(newButton)
                }
            },
            error: function (result) {
                alert('error');
            }
        });
});


function setSubmitBtnActive() {
    btn = document.getElementById('submit_btn');
    btn.className = "btn btn-primary active";
}

function setSubmitBtnDisabled() {
    btn = document.getElementById('submit_btn');
    btn.className = "btn btn-primary disabled";
}

$('#doctor_choosing_col').on('click', 'button', function (e) {
    CURRENT_APPOINTMENT_ID = $(this).val();
    DOCTOR_WAS_CHOSEN = true;
    setSubmitBtnActive();
});


$('#submit_btn').on('click', function (e) {
    e.preventDefault();
    console.log('clicked');
    $.ajax({
        type: "GET",
        url: "/patient/appointment/",
        data: {
            appointment_id: CURRENT_APPOINTMENT_ID
        },
        success: function (result) {
            console.log(result);
            if (result == 'Yes') {
                if (window.confirm('Запись к врачу прошла успешно. Перейти к начальной странице.'))
                $.ajax({
                    type: "GET",
                    url: "/",
                    data: {
                        afterAction: 1
                    },
                    success: function (data) {
                        if (data.redirect) {
                            window.location.href = data.redirect;
                        }
                    }
                });
                else {
                    deleteDoctorsFromPage();
                    deleteAppointmentTimeFromPage();
                    setSubmitBtnDisabled();
                }
            }
            else {
                if (window.confirm('К сожалению, данный врач больше недоступен в данное время. Попробуйте снова.')) {
                    deleteDoctorsFromPage();
                    deleteAppointmentTimeFromPage();
                    setSubmitBtnDisabled();
                }
            }

        },
        error: function (result) {
            alert('Произошел сбой. Запись отменена. Попробуйте снова.');
        }
    });
});


$(document).ready(function () {
    if ($(this).width() < 1000) {
        datetime_appointment_header = $("#datetime_appointment_header").remove();
        datetime_appointment = $(".datetime_appointment").remove();

        go2appointment_datetime = $("<a href='#down'><button style='vertical-align: middle' class='btn btn-default btn-lg' doctor_id='go2appointment_datetime_btn'>Далее</button></a>");
        $(".bodies").append(go2appointment_datetime);

        moved_header = $("<a name='down' style='color: black;'><div class='row' style='margin-top: 50%' doctor_id='moved_header'></div></a>");
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
    CURRENT_DOCTOR_SPECIALIZATION = event.target.innerText;
    console.log(event.target.innerHTML);
    $.ajax({
        type: "GET",
        url: "/patient/appointment/",
        data: {
            specialization: CURRENT_DOCTOR_SPECIALIZATION
        },
        success: function (doctors) {
            console.log(CURRENT_DOCTOR_SPECIALIZATION);
            if (CURRENT_DOCTOR_SPECIALIZATION !== null)
                deleteDoctorsFromPage();
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


$("#doctors_list").click(function (event) {
    console.log(219);
   CURRENT_DOCTOR_ID = event.target.innerHTML;
   console.log(CURRENT_DOCTOR_ID);
});
