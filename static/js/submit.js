$(function() {
      var form = $('#mapping-form');
      $('.submit').click(function(e) {
        e.preventDefault();
        value = $(this).data("action");
        form.append("<input type='hidden' name='submitValue' value='" + value + "' />");
        form.submit();
      });
});