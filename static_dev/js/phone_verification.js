$(document).ready(function() {
    const countdownElement = $('#countdown');
    const linkContainer = $('#linkContainer');
    let countdownDuration = countdownElement.data('countdown-duration');
    let timerInterval;

    function startTimer() {
        let minutes, seconds;
        timerInterval = setInterval(function() {
            minutes = Math.floor(countdownDuration / 60);
            seconds = countdownDuration % 60;

            const display = minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
            countdownElement.text(display);

            if (--countdownDuration < 0) {
                clearInterval(timerInterval);
                linkContainer.show();
                countdownElement.hide();
            }
        }, 1000);
    }

    $("#repeatCallButton").click(function() {
        let data = {
            repeat_call: true
        }
        $.ajax({
            url: "/profile/phone_verification/",
            type: "GET",
            data: data,
            success: function(data) {
                countdownDuration = data.countdown;
                countdownElement.show();
                linkContainer.hide();
                startTimer();

                console.log('Повторный звонок');
            },
            error: function(xhr, status, error) {
                // Handle errors
                console.error(xhr.responseText);
            }
        });
    });

    startTimer();
});

$(document).ready(function() {

});