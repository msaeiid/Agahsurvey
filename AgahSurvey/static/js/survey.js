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


$('input[name=answersheet_date]').change(function (){
    console.log('date i changed...')
})