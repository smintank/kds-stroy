$(document).ready(function() {
    $('.show_order_popup').click(function() {
        $('#overlay').addClass('active');
        $('.order_popup').show();
    });

    $('.close').click(function() {
        $('#overlay').removeClass('active');
        $('.order_popup').hide();
    });
});