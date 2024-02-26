$(document).ready(function() {
    // Hold the header at the top of the page when the user scrolls
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

    $('.close').click(function() {
        $('#overlay').removeClass('active');
        $('.order_popup').hide();
    });

    $('.show_order_popup').click(function() {
        $('#overlay').addClass('active');
        $('.order_popup').show();
    });
});


    checkbox.addEventListener("change", function() {
        button.disabled = !this.checked;
        button.style.backgroundColor = this.checked ? "#C82027" : "#c89fa1";
    });
});
