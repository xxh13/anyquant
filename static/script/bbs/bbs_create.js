/**
 * Created by cheng on 15/11/16.
 */

$(() => {
    $("#editor").wysiwyg();

    $("#bbs_create").on("click", function () {
        var title = $("#comment_title").val();
        var content = $("#editor").html();
        var parent_id = -1;
        var category_id = $("#category option:selected").val();

        $.ajax({
            type: 'POST',
            url: '/ajax/bbs/submit/',
            data: {'title': title, 'content': content, 'parent_id': parent_id, 'category_id': category_id},
            dataType: 'json',
            success: data => {
                if (data['status'] == 'ok'){
                    top.location.href = '/bbs'
                }
            }
        });
    });
})