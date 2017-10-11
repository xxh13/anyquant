/**
 * Created by Justin on 2015/12/1.
 */


$(() => {

    $('.follow').click(function() {
        var account_id = $('#account_id').val();
        $.ajax({
            url: '/bbs/follow/',
            type: 'POST',
            data: {'account_id': account_id},
            dataType: 'json',
            success: data => {
                if(data['status'] == 'ok'){
                    $(this).notify(data['data'], {position: 'top'});
                    location.reload();
                }else{
                    $(this).notify(data['data'], {position: 'top'});
                }
            }
        })
    });

})