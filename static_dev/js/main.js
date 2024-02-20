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
    var checkbox = document.getElementById("checkBox");
    var button = document.getElementById("orderButton");

    checkbox.addEventListener("change", function() {
        button.disabled = !this.checked;
        button.style.backgroundColor = this.checked ? "#C82027" : "#c89fa1";
    });
});

$(document).ready(function() {
    $('#orderForm').submit(function(event) {
        event.preventDefault();
        $('#formContent').hide();
        $('#loadingMessage').show();
        var formData = $(this).serialize();

        $.ajax({
            type: 'POST',
            url: '',
            data: formData,
            success: function(response, status, xhr) {
                if (xhr.status === 201) {
                    $('#loadingMessage').hide();
                    $('#resultMessage').show();
                } else {
                    $('#loadingMessage').hide();
                    $('#errorMessage').show();
                }
            },
            error: function(xhr, status, error) {
                $('#loadingMessage').hide();
                $('#errorMessage').show();
            }
        });
    });
});

