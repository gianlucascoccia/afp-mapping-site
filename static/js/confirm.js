$(function() {
      var form = $('#mapping-form');
      $('.confirm').click(function(e) {
        e.preventDefault();
        value = $(this).data("action");
          if (window.confirm("Are you sure?")) {
            form.append("<input type='hidden' name='submitValue' value='" + value + "' />");
            form.submit();
          }
        });
    });