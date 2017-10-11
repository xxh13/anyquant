
$("#new_strategy_btn").on("click", function () {
    var strategy_name = $("#strategy_name_form").val();

    if (strategy_name == '') {
        $("#strategy_name_form").notify("策略名不能为空", { position: 'top' });
        return;
    }

    $.ajax({
        url: '/strategy/new/',
        type: 'POST',
        data: { 'strategy_name': strategy_name },
        dataType: 'json',
        success: data => {
            if (data['status'] == 'ok') {
                location.href = '/labs/strategy/' + data['strategy_visit_id'];
            } else {
                $("#strategy_name_form").notify(data['data'], { position: 'top' });
            }
        },
        error: data => {
            $("#strategy_name_form").notify("系统出现错误，请稍后再试", { position: 'top' });
        }
    });
});