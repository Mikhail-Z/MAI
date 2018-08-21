jsonInputData = {};
$("input[name]").each(function () {
    if ($(this).prop("name") !== 'csrfmiddlewaretoken') {
        inputName = $(this).prop("name");
        jsonInputData[inputName] = {"clickedElements": new Set(), "input": "", "textarea":""}
    }
});

function createInputFromJSON(inputName) {
    inputAndClickedData = jsonInputData[inputName];
    clickedElementsArray = [...inputAndClickedData["clickedElements"]];

    inputElement = inputAndClickedData["input"];
    textareaElement = inputAndClickedData["textarea"];
    console.log(clickedElementsArray);
    clickedElementsString = $.grep(clickedElementsArray, Boolean).join(", ");
    fullData = $.grep([clickedElementsString, inputElement, textareaElement], Boolean).join(". ");
    console.log(inputName, clickedElementsString, inputElement, textareaElement);
    $("input[name="+inputName+"]").val(fullData);
}


//Поменять у записи имя класса на имя класса с припиской active и подчеркнуть запись
function makeClassActiveAndUnderlineOrBackward(element, className, backWard) {
    element.attr("class", className);
    if (backWard === false)
        element.attr("style", "text-decoration: underline");
    else
        element.css("text-decoration", "");
}

/*Сделать первую букву заглавной*/
function capitalize(string)
{
    return string.charAt(0).toUpperCase() + string.slice(1);
}


//если кликнули по одной из записей в той группе, где только одна из всех записей может быть активна
$(document).on("click", ".choose_one_state", function () {
    inputName = $(this).parents("p").attr("class");
    className = $(this).attr("class");
    newClassName = className + "-" + "active";

    //Удаляем атрибуты "активности" у элемента, по которому кликнули до этого
    oldChosenElement = $("."+inputName).find("."+newClassName);
    makeClassActiveAndUnderlineOrBackward(oldChosenElement, className, true);

    makeClassActiveAndUnderlineOrBackward($(this), newClassName, false);

    newValue = $(this).text();

    jsonInputData[inputName].clickedElements.clear();
    jsonInputData[inputName].clickedElements.add(newValue);
});

//массивы, состоящие из тех записей, по которым кликнули в группе, где несколько записей может быть активно

//вперые кликнули по записи из группы, где несколько записей может быть активно, тем самым сделав запись активной
$(document).on("click", ".choose_several_states", function () {
    newValue = $(this).text();
    inputName = $(this).parents("p").attr("class");
    newClassName = $(this).attr("class")+"-"+"active";

    jsonInputData[inputName].clickedElements.add(newValue);
    makeClassActiveAndUnderlineOrBackward($(this), newClassName, false);
});

//повторное нажатие на запись
$(document).on("click", ".choose_several_states-active", function () {
    newValue = $(this).text();
    inputName = $(this).parents("p").attr("class");
    n = "-active".length;
    newClassName = $(this).attr("class").slice(0, -n);

    jsonInputData[inputName].clickedElements.delete(newValue);
    makeClassActiveAndUnderlineOrBackward($(this), newClassName, true);
});



$("input:not([name])").change(function () {
    inputName = $(this).parents("p").attr("class");
    text = $(this).val();
    parent = $(this).parent("span.group");
    if (parent.length) {
        left_part_text = $(this).prev().text();
        right_part_text = $(this).next().text();
        jsonInputData[inputName].input = $.grep([left_part_text, text, right_part_text], Boolean).join(" ")
    } else if (inputName)
        jsonInputData[inputName].input = text;
});

$("textarea:not([name])").change(function() {
    inputName = $(this).parents("p").attr("class");
    text = $(this).val();
    jsonInputData[inputName].textarea = text;
});


$("#main_form").submit(function () {
    for (inputName in jsonInputData) {
        createInputFromJSON(inputName);
    }
});


$("#submit_btn").click(function (e) {
    e.preventDefault();
    for (inputName in jsonInputData) {
        createInputFromJSON(inputName);
    }
    $("input[name]").each(function () {
        console.log($(this).prop("name"), $(this).prop("value"));
    });
});


$(document).on("submit", "#main_form", function (e) {
        e.preventDefault();
        $.ajax({
            url: "/doctor/review/",
            type: "POST",
            data: $("#main_form").serialize(),
            success: function (new_admission) {
                $("#myModal").modal("toggle");
                admission_blank_print_url = "/doctor/review/" + new_admission.id + "/?print=true";
                $("#print_cur_blank_btn").parent("a").attr("href", admission_blank_print_url);
                $("#not_print_cur_blank_btn").parent("a").attr("href", window.location.href);
            }
        });
    });
    $(document).on("click", "#print_cur_blank, #not_print_cur_blank", function () {
        $("#myModal").modal("close");
       window.open($(this).parent("a").href());
    });
    $(document).on("click", "#not_print_cur_blank", function () {
        $("#myModal").modal("close");
       window.location.href = $(this).parent("a").href();
    });
    $("#weight").on("input", function () {
        var height = $("#height").val();
        var weight = $("#weight").val();
        if (height !== "") {
            if (isNaN(height) || isNaN(weight))
                return;
            var bmi_val = Math.round($(this).val()/((height/100) ** 2)*100)/100;
            $("#bmi").prop("value", bmi_val);
        }
    });
    $("#height").on("input", function () {
        var weight = $("#weight").val();
        var height = $("#height").val();
        if (weight !== "") {
            if (isNaN(height) || isNaN(weight))
                return;
            var bmi_val = Math.round($(this).val()/((height/100) ** 2)*100)/100;
            $("#bmi").prop("value", bmi_val);
        }
    });
    $(".dispanserization_stage").click(function (e) {
        if (e.target.innerText == "1") {
            $(".dispanserization_only").find(".first_stage_only").css("display", "inline");
            $(".dispanserization_only").find(".second_stage_only").css("display", "none");
        } else if (e.target.innerText == "2") {
            $(".dispanserization_only").find(".first_stage_only").css("display", "none");
            $(".dispanserization_only").find(".second_stage_only").css("display", "inline");
        }
    });