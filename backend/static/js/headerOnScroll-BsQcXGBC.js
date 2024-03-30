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
  }
  close() {
    this._popup.classList.remove("popup--active");
    document.removeEventListener("keydown", this._closeEscPopup);
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
      } else if (e.target.classList.contains("stock-popup")) {
        this.open();
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
