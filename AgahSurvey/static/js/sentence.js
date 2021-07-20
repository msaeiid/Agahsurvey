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

function show_question() {
    query = '#question' + current_question
    $('.questions').addClass('hide')
    $(query).removeClass('hide')
}

$('input[type=checkbox]').click(function () {
    if (this.value == 99) {
        $('input[type=checkbox][name=' + this.name + ']').prop('checked', false)
        $(this).prop('checked', true)
    } else if (this.value != 99) {
        $('input[name=' + this.name + '][value=99]').prop('checked', false)
    }
});