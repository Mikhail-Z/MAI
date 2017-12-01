function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
function csrfSaveMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
   beforeSend: function(xhr, settings) {
       if (!csrfSaveMethod(setting.type) && !this.crossDomain) {
           xhr.setRequestHeader("X-CSRFToken", csrftoken);
       }
   }
});


$('#time_choosing_col').on('click', 'button', function (e) {
    $.ajax({
            type: "GET",
            url: "/patient/appointment/",
            data: {
                spec_id:CURRENT_DOCTOR_SPECIALIZATION,
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


$("#submit_btn").click(function(e) {
    console.log("in ajax!!!");
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: $("#login_form").attr('action'),
        data: {
            login: $("#login").val(),
            password: $("#password").val(),
        }
    }).done(function (data) {
        if (data.success) {
            window.location.href = data.url;
        }
        else {
            alert("В системе нет пользователя с таким логином/паролем. Проверьте правильность вводимых данных.")
        }
    });
});