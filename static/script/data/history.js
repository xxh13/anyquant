/**
 * Created by Justin on 2015/12/18.
 */

$(() => {

    var code_list = [];

    $('input[name="raw_code"]').keyup(function() {
        var code = $(this).val();
        $.ajax({
            type: 'POST',
            url: '/editor/stock_complete',
            data: {'prefix': code},
            dataType: 'json',
            success: data => {
                var html = '';
                var length = data.length > 8 ? 8 : data.length;
                for(var i = 0; i < length; i ++) {
                    html += '<option value="' + data[i]['value'] + '">' + data[i]['meta'] + '</option>';
                    code_list[data[i]['value']] = data[i]['meta'];
                }
                document.getElementById('code_list').innerHTML = html;
            }
        });
    });

    $('#code_form').submit(function() {
        var code = $('input[name="raw_code"]').val();
        if(!code.startsWith('sh')) {
            $('input[name="code"]').val(code_list[code]);
        } else {
            $('input[name="code"]').val(code);
        }
        $(this).submit();
    });

})