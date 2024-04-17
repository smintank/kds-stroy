const __defProp = Object.defineProperty;
const __defNormalProp = (obj, key, value) => key in obj ? __defProp(obj, key, {
  enumerable: true,
  configurable: true,
  writable: true,
  value
}) : obj[key] = value;
const __publicField = (obj, key, value) => {
  __defNormalProp(obj, typeof key !== "symbol" ? key + "" : key, value);
  return value;
};

class Popup {
  constructor(popupSelector) {
    __publicField(this, "_closeEscPopup", (e) => {
      if (e.key === "Escape") {
        this.close();
      }
    });
    this._popup = document.querySelector(popupSelector);
  }
  open() {
    this._popup.classList.add("popup--active");
    document.addEventListener("keydown", this._closeEscPopup);
    document.querySelector("body").style.overflow = "hidden";
  }
  close() {
    this._popup.classList.remove("popup--active");
    document.removeEventListener("keydown", this._closeEscPopup);
    document.querySelector("body").style.overflow = "auto";

    if (document.getElementById('autocomplete-dropdown')) {
      document.getElementById('autocomplete-dropdown').style.display = 'none';
    }
  }
  setEventListeners() {
    this._popup.addEventListener("mousedown", (e) => {
      if (e.target.classList.contains("popup--active") || e.target.classList.contains("popup__close")) {
        this.close();
      }
    });
  }
}

class MessagePopup extends Popup {
  open(message, text) {
    super.open();
    this.update(message, text);
  }
  close() {
    super.close();
    this.update("", "")
  }
  update(message, text) {
    this._popup.querySelector(".popup__title").textContent = message;
    if (text) this._popup.querySelector(".popup__text").textContent = text;
  }
}

class PromotionPopup {
  constructor(popupSelector) {
    this._popup = document.querySelector(popupSelector);
  }
  open() {
    this._popup.classList.add("stock-popup--active");
  }
  close() {
    this._popup.classList.remove("stock-popup--active");
  }
  setEventListeners() {
    this._popup.addEventListener("mousedown", (e) => {
      if (e.target.classList.contains("stock-popup__close")) {
        this.close();
        setCookie("promo_popup_hide", true, 1);
      } else if (e.target.classList.contains("stock-popup")) {
        this.open();
        setCookie("promo_popup_hide", false, 1);
      }
    });
  }
}

function setCookie(cname, cvalue, exdays) {
  const d = /* @__PURE__ */ new Date();
  d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1e3);
  const expires = "expires=" + d.toUTCString();
  document.cookie = cname + "=" + cvalue + "; " + expires;
}

function getCookie(cname) {
  const name = cname + "=";
  const ca = document.cookie.split(";");
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) === " ")
      c = c.substring(1);
    if (c.indexOf(name) === 0)
      return c.substring(name.length, c.length);
  }
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

const useHeaderOnScroll = () => {
  const header = document.querySelector(".header");
  window.addEventListener("scroll", function() {
    const scrollPos = window.scrollY;
    if (scrollPos >= 1) {
      header.classList.add("header--with-border");
    } else {
      header.classList.remove("header--with-border");
    }
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

const useActiveNavSection = () => {
  const navLinks = document.querySelectorAll(".header__nav-list-item a");
  const headerHeight = document.querySelector(".header").offsetHeight;
  window.onscroll = function() {
    navLinks.forEach((navLink) => {
      if (navLink.getAttribute("href") === "#")
        return;
      const section = document.querySelector(navLink.getAttribute("href"));
      if (section.offsetTop - headerHeight <= window.scrollY && section.offsetTop + section.offsetHeight > window.scrollY) {
        navLink.classList.add("header__nav-list-item--active");
      } else {
        navLink.classList.remove("header__nav-list-item--active");
      }
    });
  };
};

export {
  Popup as P,
  MessagePopup as MP,
  PromotionPopup as PP,
  useHeaderOnScroll as a,
  useBurger as u,
  setCookie as s,
  getCookie as g,
  useCookieBanner as c,
  useActiveNavSection as n,
};
