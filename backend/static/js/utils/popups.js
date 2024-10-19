import {gC as getCookie, sC as setCookie} from './base.js';

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
    if (!getCookie("promo_popup_hide")) {
      this.open()
    }
  }
  open() {
    this._popup.classList.add("stock-popup--active");
    setCookie("promo_popup_hide", false, 1);
  }
  close() {
    this._popup.classList.remove("stock-popup--active");
    setCookie("promo_popup_hide", true, 1);
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

const popupMessage = new MessagePopup("#popup-message");
if (document.querySelector("#popup-message")) popupMessage.setEventListeners();

const usePromotionPopup = () => {
  if (document.querySelector("#popup-promotion")) {
    new PromotionPopup("#popup-promotion").setEventListeners();
  }
};

export {
  usePromotionPopup as uPP,
  popupMessage as MP,
  MessagePopup as M,
  Popup as P,
};