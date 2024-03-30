import "./modulepreload-polyfill-BoyGcPDr.js";
import { u as useBurger, a as useHeaderOnScroll, P as Popup } from "./headerOnScroll-BsQcXGBC.js";
import { u as useShowcaseModal } from "./showcaseModal-BGg2r-Tz.js";
import { u as useInputPhoneMask } from "./useInputPhoneMask-CE77khD0.js";
const useAccountItem = () => {
  const accountItems = document.querySelectorAll(".applications__list-item");
  console.log(accountItems);
  accountItems.forEach((item) => {
    item.addEventListener("click", (e) => {
      if (item.classList.contains("applications__list-item--open")) {
        return;
      }
      accountItems.forEach((item2) => {
        item2.classList.remove("applications__list-item--open");
      });
      item.classList.add("applications__list-item--open");
    });
  });
};
addEventListener("DOMContentLoaded", () => {
  useBurger();
  useHeaderOnScroll();
  useInputPhoneMask();
  useAccountItem();
  useShowcaseModal();
  const popupSuccess = new Popup("#popup-success");
  popupSuccess.setEventListeners();
  const popupFailure = new Popup("#popup-failure");
  popupFailure.setEventListeners();
  const popupAuth = new Popup("#popup-auth");
  popupAuth.setEventListeners();
  const signInButton = document.querySelector("#signIn");
  signInButton.addEventListener("click", () => popupAuth.open());
  const formAccount = document.querySelector("#formAccount");
  formAccount.addEventListener("submit", (e) => {
    e.preventDefault();
    popupSuccess.open();
    formRegister.reset();
  });
});
