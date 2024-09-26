import "../utils/modulepreload-polyfill.js";
import {
  u as useBurger,
  a as useHeaderOnScroll,
  c as useCookieBanner
} from "../utils/base.js";
import { u as useInputPhoneMask } from "../utils/input-phone-mask.js";
import { uOP as useOrderPopup } from "../utils/orders.js";
import { uPP as usePromotionPopup } from "../utils/popups.js";
import { Au as useAuthPopup } from "../utils/auth.js";
import { SI as useSmsInput } from "../utils/smscode_input.js";

const useSMSVerificationTimer = () => {
  const countdownElement = document.getElementById('countdown');
  const countdownBlock = document.getElementById('countdownBlock');
  const repeatButton = document.getElementById("repeatCallButton");
  let countdownDuration = parseInt(countdownElement.dataset.countdownDuration);
  let timerInterval;

  function startTimer() {
    let minutes, seconds;
    timerInterval = setInterval(function () {
      minutes = Math.floor(countdownDuration / 60);
      seconds = countdownDuration % 60;

      countdownElement.textContent = minutes + ':' + (seconds < 10 ? '0' : '') + seconds;

      if (--countdownDuration < 0) {
        clearInterval(timerInterval);
        repeatButton.style.display = 'block';
        countdownBlock.style.display = 'none';
      }
    }, 1000);
    if (countdownDuration > 0) {
      repeatButton.style.display = "none";
    }
  }

  document.getElementById("repeatCallButton").addEventListener("click", function () {
    fetch("/profile/phone_verification/?repeat_call=true")
      .then(response => response.json())
      .then(data => {
        countdownDuration = data.countdown;
        countdownBlock.style.display = 'block';
        repeatButton.style.display = 'none';
        document.querySelectorAll('.inputs input').forEach((input) => {
          input.disabled = false
        });
        document.querySelector('.errorlist').style.display = "none"
        startTimer();
      })
      .catch(error => {
        console.error('Error:', error);
      });
  });

  startTimer();
}

addEventListener("DOMContentLoaded", () => {
  useBurger();
  useHeaderOnScroll(true);
  useInputPhoneMask();
  useOrderPopup();
  useCookieBanner();
  usePromotionPopup();
  useAuthPopup();
  useSmsInput();
  useSMSVerificationTimer();
});
