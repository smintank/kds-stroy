import "../utils/modulepreload-polyfill.js";
import { u as useBurger, a as useHeaderOnScroll, uCS as useCitySuggestions} from "../utils/base.js";
import { u as useShowcaseModal } from "../utils/showcase-modal.js";
import { u as useInputPhoneMask } from "../utils/input-phone-mask.js";
import { uOP as useOrderPopup} from "../utils/orders.js";
import { Au as useAuthPopup } from "../utils/auth.js";

const useAccountItem = () => {
  const accountItems = document.querySelectorAll(".applications__list-item");
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
  useOrderPopup();
  useInputPhoneMask();
  useAccountItem();
  useShowcaseModal();
  useAuthPopup();
  useCitySuggestions();
});
