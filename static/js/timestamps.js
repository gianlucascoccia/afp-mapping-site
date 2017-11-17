$(function() {
        $('.timestamp :first-child').click(function(){
            var row_id = $($(this)[0]).parent().data("row");
            var col_id = $(this)[0].value;
            var appname = $('#appname').attr('value');
            var input_id = row_id + col_id;
            var timestamp = Date.now();
            $.getJSON("/store-ts/" + appname,
                       {'timestamp': timestamp, 'clicked': input_id},
                       function(data, status){});
        })
    });