/**
 * Created by cheng on 15/11/14.
 */

$(() => {
    $("#editor").wysiwyg();

    $("#post_comment").on("click", function () {
        var content = $("#editor").html();
        var parent_id = $("#parent_id").val();
        var parent_title = $("#parent_title").val();
        var code = $("#captcha_code").val();

        var post_data = { 'content': content, 'title': 'Re: ' + parent_title,
            'parent_id': parent_id, 'code': code };
        $.ajax({
            type: 'POST',
            url: '/ajax/bbs/submit/',
            data: post_data,
            dataType: 'json',
            success: data => {
                if (data['status'] == 'ok') {
                    $("#reply_comment").notify("回复成功， 如无显示请刷新页面!", { position: 'top' });
                } else {
                    $("#reply_comment").notify(data['data'], { position: 'top' });
                }
            }
        });
    });
});