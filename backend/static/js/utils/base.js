import {dM as DropdownMenu} from "./dropdown-menu.js";

function setCookie(name, value, days, path, domain, secure) {
    let expires = "";

    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }

  document.cookie = name + "=" + (value || "") + expires +
      (path ? "; path=" + path : '; path=/') +
      (domain ? "; domain=" + domain : "") + "; secure";
}

function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    if (match) return match[2];
    return false;
}

const useBurger = () => {
  const burgerBtnWrapper = document.querySelector(".header__burger-wrapper");
  const navLinks = document.querySelectorAll(".header__nav-list-item a");
  const burgerBtn = document.querySelector(".burger");
  const header = document.querySelector(".header");
  burgerBtnWrapper.addEventListener("click", () => {
    burgerBtn.classList.toggle("burger--active");
    header.classList.toggle("header--active");
  });
  navLinks.forEach((navLink) => {
    navLink.addEventListener("click", () => {
      burgerBtn.classList.remove("burger--active");
      header.classList.remove("header--active");
    });
  });
};

const useCookieBanner = () => {
  const cookieBanner = document.getElementById('cookieBanner');
  if (!getCookie('acceptedCookies')) cookieBanner.style.display = 'flex';

  document.getElementById('acceptCookies').addEventListener("click", function() {
    setCookie('acceptedCookies', true, 365); // Expires in 365 days
    cookieBanner.style.display = 'none';
  });
};

const useHeaderOnScroll = (isOff) => {
  const header = document.querySelector(".header");
  if (isOff) {
    header.classList.add("header--with-border");
    return;
  }
  window.addEventListener("scroll", function() {
    const scrollPos = window.scrollY;
    if (scrollPos >= 1) {
      header.classList.add("header--with-border");
    } else {
      header.classList.remove("header--with-border");
    }
  });
};

const useCitySuggestions = () => {
  document.querySelectorAll(".city-input").forEach(input => {
    const dropdown = new DropdownMenu(input);
    input.form.addEventListener('submit', function(event) {
      if (dropdown.chosenId === null || input.value === '') {
        input.value = '';
      } else {
        input.value = dropdown.chosenId;
      }
    });
  });
};

export {
  useHeaderOnScroll as a,
  useBurger as u,
  setCookie as sC,
  getCookie as gC,
  useCookieBanner as c,
  useCitySuggestions as uCS
};
