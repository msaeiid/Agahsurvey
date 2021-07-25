let previous_btn = $('#previous')
let next_btn = $('#next')
let current_question = parseInt($('input[name=first_question]').val())
let first_question = parseInt($('input[name=first_question]').val())
let last_question = parseInt($('input[name=last_question]').val())
previous_btn.click(function () {
    if (current_question == first_question) {
        current_question = last_question
    } else {
        current_question -= 1
    }
    show_question()
})
next_btn.click(function () {
    if (current_question == last_question) {
        current_question = first_question
    } else {
        current_question += 1
    }
    show_question()
})
let controller = {}
$(document).ready(function () {
    for (var i = first_question; i <= last_question; i++) {
        controller[i] = false
    }
})

$('input[type=checkbox]').on("change", function (event) {
    if (this.checked) {
        controller[this.name] = true
    }
    var result = true
    for (var item in controller) {
        if (controller[item] == false) {
            result = false
        }
    }
    if (result == true) {
        $('#submit').removeClass('hide')
    }
});

function show_question() {
    query = '#question' + current_question
    $('.questions').addClass('hide').fadeOut(200)
    $(query).removeClass('hide').fadeIn(200)
}

$('input[type=checkbox]').click(function () {
    if (this.value == 99) {
        $('input[type=checkbox][name=' + this.name + ']').prop('checked', false)
        $(this).prop('checked', true)
    } else if (this.value != 99) {
        $('input[name=' + this.name + '][value=99]').prop('checked', false)
    }
});