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

function setCookie(cname, cvalue, exdays) {
  const d = /* @__PURE__ */ new Date();
  d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1e3);
  const expires = "expires=" + d.toUTCString();
  document.cookie = cname + "=" + cvalue + "; " + expires;
}

const body = document.querySelector("body");

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
    body.style.overflow = "hidden";
  }
  close() {
    this._popup.classList.remove("popup--active");
    document.removeEventListener("keydown", this._closeEscPopup);
    body.style.overflow = "auto";
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
const useBurger = () => {
  const burgerBtnWrapper = document.querySelector(".header__burger-wrapper");
  const burgerBtn = document.querySelector(".burger");
  const header = document.querySelector(".header");
  burgerBtnWrapper.addEventListener("click", () => {
    burgerBtn.classList.toggle("burger--active");
    header.classList.toggle("header--active");
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
export {
  Popup as P,
  PromotionPopup as PP,
  useHeaderOnScroll as a,
  useBurger as u
};
