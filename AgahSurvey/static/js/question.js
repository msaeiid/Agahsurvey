const child = $('.child')

function show_child(number_of_child) {
    let table_place = $('.table_place')
    if (number_of_child > 0) {
        result = '<table style="border: none" class="table"><thead><tr><th>فرزند</th><th>جنسیت</th><th>سال تولد</th><th>محاسبه سن اتومات</th></tr></thead><tbody>'
        for (let i = 1; i <= number_of_child; i++) {
            result += '<tr><td>' + i + '</td>' +
                '<td><select class="form-select" name="gender_' + i + '"><option value="male">پسر</option><option value="female">دختر</option></select></td>' +
                '<td><input type="number" class="year form-control" name="year_' + i + '" placeholder="سال تولد" maxlength="4"></td>' +
                '<td><input class="form-control" type="text" name="age_' + i + '" disabled></td>' +
                '</tr>'
        }
        result += '</tbody></table>'
        table_place
        table_place.html(result).fadeIn(500)
    } else {

        table_place.html('').fadeOut(500)
    }
    let years = $('input.year')
    years.keyup(function () {
        if (this.value.length == 4) {
            var result
            var serializedData = $(this).serialize();
            $.ajax({
                url: '/survey/question/get_age/',
                data: serializedData,
                async: false,
                success: function (response) {
                    result = JSON.stringify(response['age'])
                }
            });
            console.log(result)
            if (this.name == 'year_1') {
                $('input[name=age_1]').val(result)

            } else if (this.name == 'year_2') {
                $('input[name=age_2]').val(result)

            } else if (this.name == 'year_3') {
                $('input[name=age_3]').val(result)

            }
        }
    })
}

child.keyup(function () {
    let row_number = 3
    if (this.value < 3) {
        row_number = this.value
    }
    show_child(row_number)
});

let marriage_status = $('select[name=marriage_answer]')
marriage_status.change(function () {
    if (this.value == 2 || this.value == 3 || this.value == 4) {
        $('div .children').fadeIn(500).removeClass('hide')
    } else {
        $('div .children').fadeOut(500).addClass('hide')
    }
});