$(function() {
      var href = $('.confirm').attr('href');
      $('.confirm').click(function(e) {
        e.preventDefault();
          if (window.confirm("Are you sure you want to proceed? You won't be able to go back")) {
            location.href = href;
          }
        });
    });