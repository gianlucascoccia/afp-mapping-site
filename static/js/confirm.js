$(function() {
      var form = $('#mapping-form');
      $('.confirm').click(function(e) {
        e.preventDefault();
        value = $(this).data("action");
        if (value == "submit"){
            message = "Are you sure you want to proceed? You won't be able to go back."
        } else {
            row_num = value.substr(4, value.length);
            message = "Are you sure you want to delete the row " + row_num + "?";
        }
          if (window.confirm(message)) {
            form.append("<input type='hidden' name='submitValue' value='" + value + "' />");
            form.submit();
          }
        });
    });