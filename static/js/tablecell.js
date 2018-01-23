$(function() {
    $('.timestamp :first-child').click(function(e){
        e.stopPropagation();
        var firstChild = $(this).children(":first")[0];
        if(typeof firstChild != 'undefined'){
            element = firstChild;
            $(element).prop("checked", !$(element).prop("checked"));
        } else {
            element = this;
        }
        var row_id = $(element).parent().parent().data("row");
        var col_id = element.value;
        var appname = $('#appname').attr('value');
        var input_id = row_id + col_id;
        var timestamp = Date.now();
        $.getJSON("/store-ts/" + appname,
                 {'timestamp': timestamp, 'clicked': input_id},
                 function(data, status){});
    })
});