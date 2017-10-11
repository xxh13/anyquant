/**
 * Created by Justin on 2015/12/21.
 */

$(() => {

    $(".form-datetime").datepicker({
        setDate: new Date(),
        autoclose: true,
        format: 'yyyy-mm-dd'
    });
    $("#start_time").datepicker("update", new Date());
    $("#end_time").datepicker("update", new Date());

    $("#start_time").change(function () {
        var start = $(this).val();
        $('a').each(function () {
            var href = $(this).attr('href');
            href = href.substr(0, href.indexOf('&start=') + 7) + start + href.substr(href.indexOf('&start=') + 17);
            $(this).attr('href', href);
        });
    });

    $("#end_time").change(function () {
        var end = $(this).val();
        $('a').each(function () {
            var href = $(this).attr('href');
            href = href.substr(0, href.indexOf('&end=') + 5) + end + href.substr(href.indexOf('&end=') + 15);
            $(this).attr('href', href);
        });
    });
});