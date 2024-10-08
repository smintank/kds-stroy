document.addEventListener("DOMContentLoaded", function() {
    const countdownElement = document.getElementById('countdown');
    const linkContainer = document.getElementById('linkContainer');
    let countdownDuration = parseInt(countdownElement.dataset.countdownDuration);
    let timerInterval;

    function startTimer() {
        let minutes, seconds;
        timerInterval = setInterval(function() {
            minutes = Math.floor(countdownDuration / 60);
            seconds = countdownDuration % 60;

            countdownElement.textContent = minutes + ':' + (seconds < 10 ? '0' : '') + seconds;

            if (--countdownDuration < 0) {
                clearInterval(timerInterval);
                linkContainer.style.display = 'block';
                countdownElement.style.display = 'none';
            }
        }, 1000);
    }

    document.getElementById("repeatCallButton").addEventListener("click", function() {
        let data = {
            repeat_call: true
        };
        fetch("/profile/phone_verification/?repeat_call=true")
            .then(response => response.json())
            .then(data => {
                countdownDuration = data.countdown;
                countdownElement.style.display = 'block';
                linkContainer.style.display = 'none';
                startTimer();
                console.log('Повторный звонок');
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });

    startTimer();
});
