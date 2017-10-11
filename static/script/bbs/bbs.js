/**
 * Created by cheng on 15/11/15.
 */

$(() => {
    hljs.initHighlightingOnLoad();
    $(".comment_star").on("click", function(){
        var comment_id = $(this).parent().find('input').val();

        $.ajax({
            url: '/ajax/bbs/star/',
            type: 'POST',
            data: {'comment_id': comment_id},
            dataType: 'json',
            success: data => {
                if(data['status'] == 'ok'){
                    $(this).html('<i class="icon-thumbs-up" style="margin-right: 5px;"></i>' + data['count']);
                }else{
                    $(this).notify(data['data'], {position: 'top'});
                }
            }
        })
    });

})