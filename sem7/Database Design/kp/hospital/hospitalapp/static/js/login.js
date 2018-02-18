var activeInputId;

$("#password, #login").click(function () {
    activeInputId = $(this).attr("id");
    console.log(activeInputId)
});

$("#showOrHidePasswordBtn").click(function () {
    password_input = $("#password");
    if (password_input.attr("type") === "password") {
        password_input.attr("type", "text");
        $(this).find("span").attr("class", "text-muted glyphicon glyphicon-eye-close");
    } else {
        password_input.attr("type", "password");
        $(this).find("span").attr("class", "text-muted glyphicon glyphicon-eye-open");
    }
});

$("#submit_btn").on('click', function (event) {
    event.preventDefault();
    $.ajax({
        type: "POST",
        url: "/patient/login/",
        data: {
            login: $("#login").val(),
            password: $("#password").val(),
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
        }, success: function (response) {
            if (response["status"] === "FAIL" && !document.getElementById("warning_msg")) {
                warning = $("<div class='row'><span></span></div>").attr("style", "color: red");
                warning.attr("id", "warning_msg");
                warning.text("Неправильно введен логин или пароль.");
                warning.insertBefore("#submit-group");
                $("#password").val("");
            } else if (response["status"] === "OK") {
                console.log("YES");
                window.location.href = response["redirect"];
            }
        }
    });
});


$("#login, #password").keydown(function () {
    $("#warning_msg").remove();
    if ($(this) === $("#login")) {
        activeInputId = "login";
    } else {
        activeInputId = "password"
    }
});


$("#keyboard").children().click(function () {
    if ($(":focus").children().length) {
        input_id = "#" + activeInputId;
        currentText = $(input_id).val();
        newText = $(input_id).val(currentText.slice(0, -1))
    } else {
       key = $(":focus").text();
        if (activeInputId === "login" || activeInputId === "password") {
            input_id = "#" + activeInputId;
            currentText = $(input_id).val();
            newText = $(input_id).val(currentText + key);
        }
    }

});
