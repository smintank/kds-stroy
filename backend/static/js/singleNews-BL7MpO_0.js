import "./modulepreload-polyfill-BoyGcPDr.js";
import { u as useBurger, a as useHeaderOnScroll, P as Popup } from "./headerOnScroll-BsQcXGBC.js";
import { c as useSingleNewsSlider } from "./sliders-C0i03PCH.js";
addEventListener("DOMContentLoaded", () => {
  useBurger();
  useHeaderOnScroll();
  useSingleNewsSlider();
  const popupAuth = new Popup("#popup-auth");
  popupAuth.setEventListeners();
  const signInButton = document.querySelector("#signIn");
  signInButton.addEventListener("click", () => popupAuth.open());
});
