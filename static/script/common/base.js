/**
 * Created by cheng on 15/11/18.
 */

$(() => {
    $("#feedback_post").on("click", function(){
        var feedback_content = $("#feedback_area").val();

        $.post('/feedback/',
            {'feedback_content': feedback_content},
        function(data){
            $("#feedback_modal").modal('hide');
        });

    });

    $("#captcha_img").on("click", function(){
        $(this).attr("src", $(this).attr("src") + "?code=" + Math.random());
    });
})