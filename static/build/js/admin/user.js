$(() => {
    $(".comment_del").on("click", function () {
        var strategy_id = $(this).parent().find('input').val();

        $.ajax({
            url: '/admin/user_del',
            type: 'POST',
            data: { 'id': strategy_id },
            dataType: 'json',
            success: data => {
                if (data['status'] == 'ok') {
                    $(this).parent().hide('slow');
                } else {
                    $(this).notify(data['data'], { position: 'top' });
                }
            }
        });
    });
});