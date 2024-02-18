document.addEventListener("DOMContentLoaded",function() {
    let header = $('.header');
    let headerHeight = header.height();
     
    $(window).scroll(function() {
        if($(this).scrollTop() > 1) {
            header.addClass('header_fixed');
            $('body').css({'paddingTop': headerHeight+'px'});
        } else {
            header.removeClass('header_fixed');
            $('body').css({'paddingTop': 0})
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
  var checkbox = document.getElementById("checkbox");
  var button = document.getElementById("order_button");

  checkbox.addEventListener("change", function() {
    button.disabled = !this.checked;
    button.style.backgroundColor = this.checked ? "#C82027" : "#c89fa1";
  });
});

