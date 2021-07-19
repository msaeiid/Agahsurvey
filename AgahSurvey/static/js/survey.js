let interviewer_code = $('.interviewer_code')
interviewer_code.keyup(function () {
    if (this.value.length == 5) {
        $('.interviewer_code_error').addClass('hide')
        var serializedData = $(this).serialize();
        $.ajax({
            url: '/survey/interviewer/get_name/',
            data: serializedData,
            success: function (response) {
                let text = JSON.stringify(response['name'])
                $('.interviewer_name').val(JSON.stringify(response['name']))
            },
            error: function (response) {
                console.log('error')
                alert(response["responseJSON"]["error"]);
                //$('.interviewer_name').val(JSON.stringify(response['error']))
            }
        });
    } else {
        $('.interviewer_code_error').removeClass('hide')
    }
})