$(document).ready(function(){
    $('.dropdown-toggle').dropdown();
});

$("#algo_list table tbody .hook").on("click", function(){
    var link = $(this).parent().find(".algo-name a").attr("href");
    window.location.href = link;
})

$("#new_strategy_btn").on("click", function(){
    var strategy_name = $("#strategy_name_form").val();

    if(strategy_name == ''){
        $("#strategy_name_form").notify("策略名不能为空", {position: 'top'});
        return;
    }

    $.ajax({
        url: '/strategy/new/',
        type: 'POST',
        data: {'strategy_name': strategy_name},
        dataType: 'json',
        success: data => {
            if(data['status'] == 'ok'){
                location.href = '/labs/strategy/' + data['strategy_visit_id'];
            }else{
                $("#strategy_name_form").notify(data['data'], {position: 'top'});
            }
        },
        error: data => {
            $("#strategy_name_form").notify("系统出现错误，请稍后再试", {position: 'top'})
        }
    })
});


$(".edit_cate").on("click", function(){
    //modify choose_cate_tab strategy_id input 
    var strategy_id = $(this).parent().find('input[name="strategy_id"]').val();
    $("#choose_cate_tab").find('.modal-footer input[name="strat_id"]').val(strategy_id);

    //modify choose_cate_tab category_list
    var category = $(this).parent().find('input[name="strategy_cate_id"]').val();
    $('#choose_cate_list').find('li input[value='+category+']').prop('checked',true);
});


$("#remove_cate").on("click", function(){
    var cate_id = $(this).parent().find('input').val();

    $.ajax({
        url: '/strategy/cate/delete/',
        type: 'POST',
        data: {'id':cate_id},
        dataType: 'json',
        success: data => {
            if(data['status'] == 'ok'){
                window.location.href = '/labs';
            }else{
                $(this).notify(data['data'], {position: 'top'});
            }
        }
    })
});

$(".delete_strat").on("click", function(){
    var strat_id = $(this).parent().find('input[name="strategy_id"]').val();
    $('#delete_strat_modal').find('.modal-footer input[name="strat_id"]').val(strat_id);
});


$("#delete_strat").on("click", function(){
    var strat_id = $(this).parent().find('input[name="strat_id"]').val();

    $.ajax({
        url: '/strategy/delete/',
        type: 'POST',
        data: {'id':strat_id},
        dataType: 'json',
        success: data => {
            if(data['status'] == 'ok'){
                $("#delete_strat_modal").modal('hide');
                $("td[id="+strat_id+"]").parent().hide('slow');
            }else{
                $(this).notify(data['data'], {position: 'top'});
            }
        }
    })
});

$("#new_cate").on("click", function(){
    var cate_name = $("#new_cate_tab").find('input[name="cate_name"]').val();

    $.ajax({
        url: '/strategy/cate/new/',
        type: 'POST',
        data: {'name':cate_name},
        dataType: 'json',
        success: data => {
            if(data['status'] == 'ok'){

                //add list to navbar and category_list
                $("#title_dropdown ul").append("<li><a href='/labs?cate="+data['category']['visit_id']+"' class='0'>"+data['category']['name']+"</a></li>");
                $("#choose_cate_list").append("<li class='list-group-item'><input type='radio' checked='' name='list_id' value='"+data['category']['id']+"'>"+data['category']['name']+"</li>");
    
                //make choose_category tab got focus
                $(".nav-tabs a[href='#choose_cate_tab']").tab('show');
            }else{
                $(this).notify(data['data'], {position: 'top'});
            }
        }
    })
});

$('#choose_cate').on("click", function(){
    var strategy_id = $(this).parent().find('input[name="strat_id"]').val();
    var cur_cate_id = $(this).parent().find('input[name="cur_cate_id"]').val();
    var cate_id = $('#choose_cate_list input[name="list_id"]:checked').val();
    var cate_name = $('#choose_cate_list input[name="list_id"]:checked').parent().text();

    $.ajax({
        url: '/strategy/cate/movestrategy/',
        type: 'POST',
        data: {'strategy_id': strategy_id, 'cate_id': cate_id},
        dataType: 'json',
        success: data => {
            if(data['status'] == 'ok'){
                //修改当前分类信息
                $($("td[id=" + strategy_id + "]").parent().children()[3]).text(cate_name);
                $("td[id="+ strategy_id + "]").parent().children()
                    .find("input[name='strategy_cate_id']").val(cate_id);
                $("#edit_cate_modal").modal('hide');
                if(cur_cate_id != "" && cur_cate_id != cate_id){
                    $("td[id="+strategy_id+"]").parent().hide('slow');
                }
            }else{
                $(this).notify(data['data'], {position: 'top'});
            }
        }
    })
});