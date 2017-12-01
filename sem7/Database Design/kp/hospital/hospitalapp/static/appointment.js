var CURRENT_DOCTOR_SPECIALIZATION;
var CURRENT_APPOINTMENT_TIME;
var CURRENT_APPOINTMENT_ID;
var NUMBER_OF_CHOSEN_ELEMENTS;

var APPOINTMENT_TIME_WAS_CHOSEN = false;
var SPECIALIZATION_WAS_CHOSEN = false;
var DOCTOR_WAS_CHOSEN = false;

function insertAfter(newNode, referenceNode) {
  referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

function deleteAppointmentTimeFromPage() {

    time_choosing_col = document.getElementById('time_choosing_col');
    while (time_choosing_col.childElementCount != 1) {
        time_choosing_col.removeChild(time_choosing_col.children[1])
    }
}

function deleteDoctorsFromPage() {
    doctor_choosing_col = document.getElementById('doctor_choosing_col');
    while (doctor_choosing_col.childElementCount != 1) {
        doctor_choosing_col.removeChild(doctor_choosing_col.children[1])
    }
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
            specialization_id: $(this).val(), // < note use of 'this' here
        },
        success: function (result) {
            for (var i in result) {
                newButton = document.createElement("button");
                newButton.className = "btn btn-default";
                newButton.innerText = result[i].appointment_time;
                newButton.value = result[i].appointment_time;
                insertAfter(newButton, document.getElementById('time_choosing_col').firstElementChild);
            }
        },
        error: function (result) {
            alert('error');
        }
    });
});


$('#time_choosing_col').on('click', 'button', function (e) {
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
                    newButton.innerText = result[i].employee__last_name+" "+result[i].employee__first_name+" "+result[i].employee__patronymic;
                    newButton.value = result[i].appointment_id;
                    insertAfter(newButton, document.getElementById('doctor_choosing_col').firstElementChild);
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