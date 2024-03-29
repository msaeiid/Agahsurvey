let current_direction
let next_btn = $('#next_btn')
let previous_btn = $('#previous_btn')
let options_html = $('#options')
let questions_html = $('#questions')
let current_question = parseInt($('input[name=first_question]').val())
let first_question = parseInt($('input[name=first_question]').val())
let last_question = parseInt($('input[name=last_question]').val())
let submit_btn = $('#submit')
//form submit...
$('#submit').click(function () {
    $('#submit').addClass('hide')
})
$('form').submit(function () {
    let A1 = localStorage.getItem("A1")
    let A2 = localStorage.getItem("A2")
    let A4 = localStorage.getItem("A4")
    let A6 = localStorage.getItem("A6")
    let A7 = localStorage.getItem("A7")
    let A8 = localStorage.getItem("A8")
    let A9 = localStorage.getItem("A9")
    let A10 = localStorage.getItem("A10")
    let A11 = localStorage.getItem("A11")
    let A12 = localStorage.getItem("A12")
    let answersheet = $('input[name=answersheet]').val()
    let last_question = $('input[name=last_question]').val()
    let first_question = $('input[name=first_question]').val()
    $.ajax({
        url: '/survey/brands_answer_questions/',
        data: {
            'answersheet': answersheet,
            'last_question': last_question,
            'first_question': first_question,
            'A1': A1,
            'A2': A2,
            'A4': A4,
            'A6': A6,
            'A7': A7,
            'A8': A8,
            'A9': A9,
            'A10': A10,
            'A11': A11,
            'A12': A12,
        },
        async: false,
        success: function () {
            console.log('ajax success')
            //$('form').submit();
        }
    });
});
//form submit...

$(document).ready(function () {
    fetch_data_from_server()
});

function fetch_data_from_server() {
    let serialized_current = $($('input[name=first_question]')).serialize()
    $.ajax({
        url: '/survey/brands_brands_list/',
        dataType: "json",
        data: serialized_current,
        success: function (response) {
            localStorage.setItem('options', JSON.stringify(response))
        }
    });
    let data = {'first_question': first_question}
    $.ajax({
        url: '/survey/brands_questions_list/',
        dataType: "json",
        data: data,
        success: function (response) {
            localStorage.setItem('questions', JSON.stringify(response))
        }
    });
}

$(document).ajaxSuccess(function () {
    question_management('next')
    paging('next')
    previous_btn.addClass('hide')
})
next_btn.click(function () {
    //چک میکنم که به سوال آخر رسیدم submit کنم
    if (current_question > last_question) {
        next_btn.addClass('hide')
        submit_btn.removeClass('hide')
    }
    //checkbox های تیک خورده را پیدا میکنم
    let answer = document.querySelectorAll('input:checked')
    if (answer.length == 0) {
        answer = document.querySelectorAll('input[type=number]')
    }
    if (answer.length == 0) {
        answer = $('select')
    }


    //بخش گزینه های سوال قبلی را پاک میکنم
    options_html.fadeOut(2).html('')
    questions_html.fadeOut(2).html('')
    next_btn.fadeOut(2)
    previous_btn.fadeOut(2)
    if (current_direction == 'previous') {
        //صفحه را refresh به بعد میکنم
        paging('next')
    }
    // به سوال بعدی بروم
    question_management('next', answer)
    //صفحه را refresh به بعد میکنم
    paging('next')
});

previous_btn.click(function () {
    //بخش گزینه های سوال قبلی را پاک میکنم
    options_html.fadeOut(2).html('')
    questions_html.fadeOut(2).html('')
    next_btn.fadeOut(2)
    previous_btn.fadeOut(2)
    //صفحه را refresh به قبل میکنم
    paging('previous')
    // به سوال قبل بروم
    question_management('previous')
});

function get_data_localstorage(data) {
    return JSON.parse(localStorage.getItem(data))
}

function question_management(next_or_previous, answer = undefined) {

    if (current_question == 8) {
        //question8
        if (next_or_previous == 'previous') {
            fetch_data_from_server()
        }
        let brands = JSON.parse(localStorage.options).options
        options_show(brands, 'brands')
        let radiobuttnons = $('input[type=checkbox]')
        radiobuttnons.on('change', function (e) {
            if ($('input[type=checkbox]:checked').length > 1) {
                $(this).prop('checked', false);
                alert('لطفا فقط یک برند را انتخاب کنید')
            }
        });
    } else if (current_question == 9) {
        //question9
        let temp
        if (next_or_previous == 'next') {
            temp = set_data_localstorage(answer, 'A1')
        } else {
            temp = get_data_localstorage('A1')
        }
        let brands = JSON.parse(localStorage.options).options
        if (answer != 99) {
            let index
            for (var key in temp) {
                index = temp[key]
            }
            if (index != undefined) {
                let temp1 = brands.splice(0, index - 1)
                let temp2 = brands.splice(1, brands.length)
                brands = temp1.concat(temp2)
                localStorage.removeItem('brands')
                localStorage.setItem('brands', JSON.stringify(brands))
            }
        }
        options_show(brands, 'brands')
    } else if (current_question == 10) {
        //question10
        let temp
        if (next_or_previous == 'next') {
            temp = set_data_localstorage(answer, 'A2')
            let A1 = JSON.parse(localStorage.A1)
            $.extend(temp, A1)
        } else {
            temp = get_data_localstorage('A2')
        }
        options_show(temp, 'rest')
    } else if (current_question == 11) {
        //question11
        let temp
        if (next_or_previous == 'next') {
            temp = set_data_localstorage(answer, 'A4')
        } else {
            temp = get_data_localstorage('A4')
        }
        options_show(temp, 'rest')
        let radiobuttnons = $('input[type=checkbox]')
        radiobuttnons.on('change', function (e) {
            if ($('input[type=checkbox]:checked').length > 3) {
                $(this).prop('checked', false);
                alert('لطفا حداکثر سه برند را انتخاب کنید')
            }
        });
    } else if (current_question == 12) {
        //question12
        let temp
        if (next_or_previous == 'next') {
            temp = set_data_localstorage(answer, 'A6')
        } else {
            temp = get_data_localstorage('A6')
        }
        options_show(temp, 'number')
        $('.option').change(function () {
            var min = parseInt($(this).attr('min'));
            if ($(this).val() < min) {
                $(this).val(min);
            }
        });
    } else if (current_question == 13) {
        //question13
        previous_btn.removeClass('hide')
        let temp
        if (next_or_previous == 'next') {
            temp = set_data_localstorage(answer, 'A7')
        } else {
            temp = get_data_localstorage('A7')
        }
        let chart_data = []
        let chart_value = []
        let sum = 0
        for (item in temp) {
            chart_data.push(item)
            sum += parseInt(temp[item])
        }
        for (item in temp) {
            chart_value.push(parseInt(temp[item]) / sum * 100)
        }

        let A8 = {}
        for (var i = 0; i < 3; i++) {
            A8[chart_data[i]] = chart_value[i]
        }
        localStorage.setItem('A8', JSON.stringify(A8))
        let result = '<div class="row"><div class="col-lg-2 col-md-2 col-sm-12 col-12"></div><div class="col-lg-5 col-md-5 col-sm-12 col-12"><canvas id="myChart" width="400" height="400"></canvas></div></div>'
        options_html.fadeIn(400).html(result)
        next_btn.fadeIn(400)
        previous_btn.fadeIn(400)
        questions_show()
        var ctx = document.getElementById('myChart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: chart_data,
                datasets: [{
                    label: chart_data,
                    data: chart_value,
                    backgroundColor: [
                        'rgba(205, 180, 219, 1)',
                        'rgba(255, 175, 204, 1)',
                        'rgba(162, 210, 255, 1)',
                    ],
                    borderColor: [
                        'rgba(205, 180, 219, 1)',
                        'rgba(255, 175, 204, 1)',
                        'rgba(162, 210, 255, 1)',
                    ],
                    borderWidth: 1
                }]
            },
        });
    } else if (current_question == 14) {
        //question14
        //چیزی ذخیره نمیشود
        previous_btn.addClass('hide')
        options_show(JSON.parse(localStorage.A7), 'numberWithLimit')
        $('.option').change(function () {
            var max = parseInt($(this).attr('max'));
            var min = parseInt($(this).attr('min'));
            if ($(this).val() > max) {
                $(this).val(max);
            } else if ($(this).val() < min) {
                $(this).val(min);
            }
        });
    } else if (current_question == 15) {
        //question15
        let temp
        if (next_or_previous == 'next') {
            temp = set_data_localstorage(answer, 'A9')
        } else {
            temp = get_data_localstorage('A9')
        }
        options_show(JSON.parse(localStorage.A9), 'currency')
        $('.option').change(function () {
            var min = parseInt($(this).attr('min'));
            if ($(this).val() < min) {
                $(this).val(min);
            } else if ($(this).val() < 1000) {
                alert('مبلغ وارد شده کمتر از 1000 تومان میباشد')
                $(this).val(1000);
            }
        });
    } else if (current_question == 16) {
        //question16
        let temp
        if (next_or_previous == 'next') {
            temp = set_data_localstorage(answer, 'A10')
        } else {
            temp = get_data_localstorage('A10')
        }
        options_show(JSON.parse(localStorage.A6), 'option')
        let error_message = $('.error')
        $('select').change(function () {
                let selects = $('select')
                let val1 = parseInt(selects[0].value)
                let val2 = parseInt(selects[1].value)
                let val3 = parseInt(selects[2].value)
                if (val1 == val2 || val1 == val3 || val2 == val3) {
                    //تکراری هست
                    if (error_message.hasClass('hide')) {
                        //اگر خطا مخفی هست روشن کن
                        error_message.removeClass('hide')
                    }
                    if (!next_btn.hasClass('hide')) {
                        // اگر دکمه بعدی فعال هست غیر فعال کن
                        next_btn.addClass('hide')
                    }
                } else {
                    //تکراری نیست
                    if (!error_message.hasClass('hide')) {
                        //اگر خطا فعال هست غیر فعال کن
                        error_message.addClass('hide')
                    }
                    if (next_btn.hasClass('hide')) {
                        //اگر دکمه بعدی غیر فعال هست فعال کن
                        next_btn.removeClass('hide')
                    }
                }
            }
        );
    } else if (current_question == 17) {
        //question17
        let temp
        if (next_or_previous == 'next') {
            temp = set_data_localstorage(answer, 'A11')
        } else {
            temp = get_data_localstorage('A11')
        }
        options_show(JSON.parse(localStorage.A4), 'radioButton')
    } else if (current_question == 18) {
        //question18
        let temp
        if (next_or_previous == 'next') {
            temp = set_data_localstorage(answer, 'A12')
        } else {
            temp = get_data_localstorage('A12')
        }
        let result = '<h2>به منظور پاسخ مجدد به سوالات بخش آگاهی برند دکمه' +
            'F5' +
            'را فشار دهید' +
            '</h2>'
        options_html.fadeIn(400).html(result)
    }
    questions_show()
}

function paging(next_or_previous) {
    let temp;
    if (next_or_previous == 'next') {
        temp = current_question + 1
        current_direction = 'next'
    } else if (next_or_previous == 'previous') {
        if (current_direction == 'next') {
            temp = current_question - 2
        } else {
            temp = current_question - 1
        }
        current_direction = 'previous'
    }
    if (temp == 8) {
        previous_btn.addClass('hide')
    }
    current_question = temp
}

function options_show(data, type) {
    let result = ''
    let counter = 0
    if (type == 'brands') {
        for (var item in data) {
            result += '<div class="row">' +
                '<label>' +
                '<input class="form-check-input" type="checkbox" value="' + data[item].option_value + '" name="' + data[item].option_title + '" id="' + data[item].option_value + '">&nbsp;' +
                data[item].option_title +
                '</label>' +
                '</div>'
        }
    } else if (type == 'rest') {
        for (item in data) {
            result += '<div class="row">' +
                '<label>' +
                '<input class="form-check-input" type="checkbox" value="' + data[item] + '" name="' + item + '" id="flexCheckDefault">&nbsp;' +
                item +
                '</label>' +
                '</div>'
        }
    } else if (type == 'number') {
        for (item in data) {
            result += '<div class="row">' +
                '<label>' + item + ': ' +
                '<input type="number" name="' + item + '" min="0" class="option form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-sm">' +
                '</label>' +
                '</div>'
        }
    } else if (type == 'numberWithLimit') {
        for (item in data) {
            result += '<div class="row">' +
                '<label>' + item + ': ' +
                '<input min="0" max="' + data[item] + '" type="number" name="' + item + '" class="option form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-sm">' +
                '</label>' +
                '</div>'
        }
    } else if (type == 'currency') {
        for (item in data) {
            result += '<div class="row">' +
                '<label>' + item + ': ' +
                '<input placeholder="تومان" type="number" name="' + item + '" min="0" class="option form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-sm">' +
                '</label>' +
                '</div>'
        }
    } else if (type == 'option') {
        result += '<h3 class="error hide">لطفا مقادیر متفاوتی را انتخاب نمایید</h3>'
        for (item in data) {
            result += '<div class="row">' +
                '<label>' + item + ': ' +
                '<select name="' + item + '" class="form-select">' +
                '<option value="1">اول</option>' +
                '<option value="2">دوم</option>' +
                '<option value="3">سوم</option>' +
                '</select></label></div>'
        }
    } else if (type == 'radioButton') {
        result += '<div class="table-responsive"><table class="table align-middle"' +
            '<thead>' +
            '<tr>' +
            '<th scope="col">برند</th>' +
            '<th scope="col">روزی یکبار یا بیشتر</th>' +
            '<th scope="col">چهار الی پنج مرتبه در هفته</th>' +
            '<th scope="col">دو الی سه مرتبه در هفته</th>' +
            '<th scope="col">یک مرتبه در هفته</th>' +
            '<th scope="col">دو هفته یک مرتبه</th>' +
            '<th scope="col">ماهی یک مرتبه</th>' +
            '<th scope="col">هر دو الی سه ماه یک مرتبه</th>' +
            '<th scope="col">هر چهار الی شش ماه یک مرتبه</th>' +
            '<th scope="col">کمتر</th>' +
            '<th scope="col">هیچوقت</th>' +
            '<th scope="col">نمی دانم/نمی توانم بگویم</th>' +
            '</tr>' +
            '</thead>' +
            '<tbody>'
        for (item in data) {
            result +=
                '<tr>' +
                '<td scope="row">' +
                '<h6>' + item + '</h6>' +
                '</td>' +
                '<td>' +
                '<input class="form-check-input" type="radio" name="' + item + '" id="flexRadioDefault1" value="1">' +
                ' </td>' +
                '<td>' +
                '<input class="form-check-input" type="radio" name="' + item + '" id="flexRadioDefault2" value="2">' +
                ' </td>' +
                '<td>' +
                '<input class="form-check-input" type="radio" name="' + item + '" id="flexRadioDefault3" value="3">' +
                ' </td>' +
                '<td>' +
                '<input class="form-check-input" type="radio" name="' + item + '" id="flexRadioDefault4" value="4">' +
                ' </td>' +
                '<td>' +
                '<input class="form-check-input" type="radio" name="' + item + '" id="flexRadioDefault5" value="5">' +
                ' </td>' +
                '<td>' +
                '<input class="form-check-input" type="radio" name="' + item + '" id="flexRadioDefault6" value="6">' +
                ' </td>' +
                '<td>' +
                '<input class="form-check-input" type="radio" name="' + item + '" id="flexRadioDefault7" value="7">' +
                ' </td>' +
                '<td>' +
                '<input class="form-check-input" type="radio" name="' + item + '" id="flexRadioDefault8" value="8">' +
                ' </td>' +
                '<td>' +
                '<input class="form-check-input" type="radio" name="' + item + '" id="flexRadioDefault9" value="9">' +
                ' </td>' +
                '<td>' +
                '<input class="form-check-input" type="radio" name="' + item + '" id="flexRadioDefault10" value="10">' +
                ' </td>' +
                '<td>' +
                '<input class="form-check-input" type="radio" name="' + item + '" id="flexRadioDefault11" value="11">' +
                ' </td>' +
                '</tr>'
        }
        result += '</tbody></table></div>'
    }
    options_html.fadeIn(400).html(result)
    next_btn.fadeIn(400)
}

function questions_show() {
    let question = JSON.parse(localStorage.questions)
    let question_title = '<i class="fas fa-cloud"></i>&nbsp;'
    for (q in question.questions) {
        if (question.questions[q].pk == current_question) {
            question_title += question.questions[q].question_title
        }
    }
    questions_html.fadeIn(400).html(question_title)
}

function set_data_localstorage(answer, where) {
    let temp = {};
    for (var i = 0; i < answer.length; i++) {
        if (answer[i].value != 99) {
            temp[answer[i].name] = answer[i].value
        }
    }
    localStorage.setItem(where, JSON.stringify(temp))
    return temp
}