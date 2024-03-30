import "./modulepreload-polyfill-BoyGcPDr.js";
import { u as useBurger, a as useHeaderOnScroll } from "./headerOnScroll-BsQcXGBC.js";
import { u as useShowcaseModal } from "./showcaseModal-BGg2r-Tz.js";
import { u as useInputPhoneMask } from "./useInputPhoneMask-CE77khD0.js";


function setCookie(cname, cvalue, exdays) {
  const d = /* @__PURE__ */ new Date();
  d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1e3);
  const expires = "expires=" + d.toUTCString();
  document.cookie = cname + "=" + cvalue + "; " + expires;
}
function getCookie(cname) {
  const name = cname + "=";
  const ca = document.cookie.split(";");
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == " ")
      c = c.substring(1);
    if (c.indexOf(name) == 0)
      return c.substring(name.length, c.length);
  }
  return false;
}

document.addEventListener("DOMContentLoaded", function() {
    // Function to show the cookie banner if the user has not accepted cookies
    const cookieBanner = document.getElementById('cookieBanner');
    const acceptedCookies = getCookie('acceptedCookies');
    if (!acceptedCookies) cookieBanner.style.display = 'flex';

    document.getElementById('acceptCookies').addEventListener("click", function() {
        setCookie('acceptedCookies', true, 365); // Expires in 365 days
        cookieBanner.style.display = 'none';
    });
});

addEventListener("DOMContentLoaded", () => {
  useBurger();
  useHeaderOnScroll();
  useInputPhoneMask();
  useShowcaseModal();

});