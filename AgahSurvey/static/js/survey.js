let interviewer_code = $('.interviewer_code')
interviewer_code.keyup(function () {
    if (this.value.length == 5) {
        $('.interviewer_code_error').addClass('hide')
        var serializedData = $(this).serialize();
        $.ajax({
            url: '/survey/interviewer/get_name/',
            data: serializedData,
            success: function (response) {
                $('.interviewer_name').val(response['name'])
            },
            error: function (response) {
                console.log('error')
                alert(response["responseJSON"]["error"]);
                $('.interviewer_name').val('')
            }
        });
    } else {
        $('.interviewer_code_error').removeClass('hide')
    }
})

$('input[name=responder_mobile]').keyup(function () {
    if (this.value.length >= 2) {
        let temp = this.value.toString().split('').map(iNum => parseInt(iNum, 10));
        console.log(typeof (temp[0]), typeof (temp[1]))
        if (temp[0] != 0 || temp[1] != 9) {
            alert('شماره موبایل وارد شده نا معتبر است')
            $('input[name=responder_mobile]').val('')
        }
    }
})


$('input[name=answersheet_date]').change(function () {
    let temp = moment.from(this.value, 'fa', 'YYYY/M/D').format('YYYY-M-D')
    var date = new Date(temp.replace(/(\d{2})-(\d{2})-(\d{4})/, "$2/$1/$3"))
    let result
    switch (date.getDay()) {
        case 0:
            result = 'یکشنبه';
            break;
        case 1:
            result = 'دوشنبه';
            break;
        case 2:
            result = 'سه شنبه';
            break;
        case 3:
            result = 'چهارشنبه';
            break;
        case 4:
            result = 'پنجشنبه';
            break;
        case 5:
            result = 'جمعه';
            break;
        case 6:
            result = 'شنبه';
            break;
    }
    $('input[name=answersheet_day]').val(result)
})

$(document).ready($(function () {
    $('input[name=responder_name]').autocomplete({
        source: '/survey/f_name_suggest/'
    });
}));


$(document).ready($(function () {
    $('input[name=responser_family]').autocomplete({
        source: '/survey/l_name_suggest/'
    });
}));
