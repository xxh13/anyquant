$(() => {
    $(".comment_del").on("click", function () {
        var comment_id = $(this).parent().find('input').val();

        $.ajax({
            url: '/admin/bbs_del',
            type: 'POST',
            data: { 'id': comment_id },
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