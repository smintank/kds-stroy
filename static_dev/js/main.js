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


$(document).ready(function() {
    const cookieBanner = $('#cookieBanner');

    // Check if the user has accepted cookies
    const acceptedCookies = getCookie('acceptedCookies');
    if (!acceptedCookies) {
        cookieBanner.show();
    }

    // When the user clicks on the accept button
    $('#acceptCookies').click(function() {
        // Set a cookie to indicate that the user has accepted cookies
        setCookie('acceptedCookies', true, 365); // Expires in 365 days
        cookieBanner.hide();
    });

    // Function to set a cookie
    function setCookie(name, value, days) {
        let expires = "";
        if (days) {
            const date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "") + expires + "; path=/";
    }

    // Function to get a cookie
    function getCookie(name) {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    }
});
