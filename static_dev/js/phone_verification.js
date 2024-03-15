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
            }
        }, 1000);
    }

    // Start the timer when the page loads
    startTimer();
});