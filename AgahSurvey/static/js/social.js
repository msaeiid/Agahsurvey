let radiobuttnons = $('input[type=checkbox]')


$('form').submit(function () {
    console.log('click')
    $('button[type=submit]').addClass('hide')
});

radiobuttnons.on('change', function (e) {
    if ($('input[type=checkbox]:checked').length > 3) {
        $(this).prop('checked', false);
        $('.error').removeClass('hide')
        $('.error').addClass('show')
    } else {
        $('.error').addClass('hide')
        $('.error').removeClass('show')

    }
});