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


$("#backwardBtn").click(function () {
    window.history.go(-1);
});