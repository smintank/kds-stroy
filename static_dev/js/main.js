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

    $('.close, .overlay').click(function() {
        $('#overlay').removeClass('active');
        $('.order_popup').hide();
        $('.login_popup').hide();
        $('.logout_popup').hide();
        $('.photo_popup').hide();
    });

    $('.show_order_popup').click(function() {
        $('#overlay').addClass('active');
        $('.login_popup').hide();
        $('.logout_popup').hide();
        $('.order_popup').show();
    });

    $('.show_login_popup').click(function() {
        $('#overlay').addClass('active');
        $('.order_popup').hide();
        $('.login_popup').show();
    });

    $('#show_logout_popup').click(function() {
        $('#overlay').addClass('active');
        $('.order_popup').hide();
        $('.logout_popup').show();
    });

    $('#cancelLogout, #confirmLogout').click(function() {
         $('#overlay').removeClass('active');
        $('#logoutPopup').hide();
    });
});


$(document).ready(function() {
    // Function to show the cookie banner if the user has not accepted cookies
    const cookieBanner = $('#cookieBanner');

    const acceptedCookies = getCookie('acceptedCookies');
    if (!acceptedCookies) {
        cookieBanner.show();
    }

    $('#acceptCookies').click(function() {
        // Set a cookie to indicate that the user has accepted cookies
        setCookie('acceptedCookies', true, 365); // Expires in 365 days
        cookieBanner.hide();
    });

    function setCookie(name, value, days) {
        let expires = "";
        if (days) {
            const date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "") + expires + "; path=/";
    }

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


$(document).ready(function() {
    // Function to check if an element is in the viewport
    function isInViewport(element) {
        if (!element || !element.length) {
            return false;
        }
        const elementTop = element.offset().top;
        const elementBottom = elementTop + element.outerHeight();
        const viewportTop = $(window).scrollTop();
        const viewportBottom = viewportTop + $(window).height();
        return elementBottom > viewportTop && elementTop < viewportBottom;
    }

    $(window).scroll(function() {
        $('a[href="#services"], a[href="#work_steps"]').each(function() {
            const targetId = $(this).attr('href');
            const targetElement = $(targetId);
            if (isInViewport(targetElement)) {
                if (targetId === '#services') {
                    $('#headerServices').attr('class', 'header_underline');
                } else if (targetId === '#work_steps') {
                    $('#headerWorkSteps').attr('class', 'header_underline');
                }
            } else {
                if (targetId === '#services') {
                    $('#headerServices').removeAttr('class');
                } else if (targetId === '#work_steps') {
                    $('#headerWorkSteps').removeAttr('class');
                }
            }
        });
    });
});

$(document).ready(function() {
    // Function to save inputted text to localStorage
    function saveInputText(inputId, debounceTime = 500) {
        clearTimeout($(this).data('timeout'));
        const timeout = setTimeout(function() {
            const inputValue = $('#' + inputId).val();
            localStorage.setItem(inputId, inputValue);
        }, debounceTime);
        $(this).data('timeout', timeout);
    }

    function populateInputFields() {
        $('input[type="text"], textarea').each(function() {
            const inputId = $(this).attr('id');
            const savedValue = localStorage.getItem(inputId);
            if (savedValue) {
                $(this).val(savedValue);
            }
        });
    }

    populateInputFields();

    $('input[type="text"], textarea').not('.ds_input').on('input', function() {
        const inputId = $(this).attr('id');
        saveInputText(inputId);
    });
});


