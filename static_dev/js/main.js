document.addEventListener("DOMContentLoaded",function() {
    let header = $('.header');
    let headerHeight = header.height(); // вычисляем высоту шапки
     
    $(window).scroll(function() {
        if($(this).scrollTop() > 1) {
            header.addClass('header_fixed');
            $('body').css({
                'paddingTop': headerHeight+'px' // делаем отступ у body, равный высоте шапки
            });
        } else {
            header.removeClass('header_fixed');
            $('body').css({
                'paddingTop': 0 // удаляю отступ у body, равный высоте шапки
            })
        }
    });
});