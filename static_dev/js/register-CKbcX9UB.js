import "./modulepreload-polyfill-BoyGcPDr.js";
import { u as useBurger, a as useHeaderOnScroll, P as Popup } from "./headerOnScroll-BsQcXGBC.js";
import { u as useInputPhoneMask } from "./useInputPhoneMask-CE77khD0.js";
addEventListener("DOMContentLoaded", () => {
  useBurger();
  useHeaderOnScroll();
  useInputPhoneMask();
  const popupSuccess = new Popup("#popup-success");
  popupSuccess.setEventListeners();
  const popupFailure = new Popup("#popup-failure");
  popupFailure.setEventListeners();
  const popupAuth = new Popup("#popup-auth");
  popupAuth.setEventListeners();
  const signInButton = document.querySelector("#signIn");
  signInButton.addEventListener("click", () => popupAuth.open());
  // const formRegister = document.querySelector("#formRegister");
  // formRegister.addEventListener("submit", (e) => {
  //   e.preventDefault();
  //   popupSuccess.open();
  //   formRegister.reset();
  // });
});
