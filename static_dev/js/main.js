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

// $(document).ready(function() {
//     // Function to check if the current URL hash is equal to the desired anchor
//     function isAtAnchor(anchor) {
//         return window.location.hash === `#${anchor}`;
//     }
//
//     // Example usage
//     if (isAtAnchor('services')) {
//         console.log('User is at anchor #services');
//     } else if (isAtAnchor('work_steps')) {
//         console.log('User is not at anchor #work_steps');
//     }
// });

// $(document).ready(function() {
//     // Function to check if an element is in the viewport
//     function isInViewport(elem) {
//         const bounding = elem.getBoundingClientRect();
//         return (
//             bounding.top >= 0 &&
//             bounding.left >= 0 &&
//             bounding.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
//             bounding.right <= (window.innerWidth || document.documentElement.clientWidth)
//         );
//     }
//
//     // Function to get the currently visible anchor
//     function getCurrentAnchor() {
//         if (isInViewport($('#services')[0])) {
//             return '#services';
//         } else if (isInViewport($('#work_steps')[0])) {
//             return '#work_steps';
//         } else {
//             return null;
//         }
//     }
//
//     // Scroll event listener to detect changes in the currently visible anchor
//     $(window).on('scroll', function() {
//         const currentAnchor = getCurrentAnchor();
//         if (currentAnchor) {
//             console.log('User is currently at anchor:', currentAnchor);
//         }
//     });
// });

$(document).ready(function() {
    // Function to check if element is in viewport
    function isInViewport(element) {
        if (!element || !element.length) {
            return false;
        }
        var elementTop = element.offset().top;
        var elementBottom = elementTop + element.outerHeight();
        var viewportTop = $(window).scrollTop();
        var viewportBottom = viewportTop + $(window).height();
        return elementBottom > viewportTop && elementTop < viewportBottom;
    }

    $(window).scroll(function() {
        $('a[href="#services"], a[href="#work_steps"]').each(function() {
            var targetId = $(this).attr('href');
            var targetElement = $(targetId);
            if (isInViewport(targetElement)) {
                // console.log(targetId + ' is in viewport');
                if (targetId === '#services') {
                    $('#headerServices').attr('class', 'header-underline');
                } else if (targetId === '#work_steps') {
                    $('#headerWorkSteps').attr('class', 'header-underline');
                }
            } else {
                // Remove the attribute when the target is not in viewport
                if (targetId === '#services') {
                    $('#headerServices').removeAttr('class');
                } else if (targetId === '#work_steps') {
                    $('#headerWorkSteps').removeAttr('class');
                }
            }
        });
    });
});