import "../utils/modulepreload-polyfill.js";
import { u as useBurger, a as useHeaderOnScroll, c as useCookieBanner } from "../utils/base.js";
import { u as useShowcaseModal } from "../utils/showcase-modal.js";
import { u as useInputPhoneMask } from "../utils/input-phone-mask.js";
import { uPP as usePromotionPopup } from "../utils/popups.js";
import { uOP as useOrderPopup } from "../utils/orders.js";
import { Au as useAuthPopup } from "../utils/auth.js";


addEventListener("DOMContentLoaded", () => {
  useBurger();
  useHeaderOnScroll(true);
  useInputPhoneMask();
  useShowcaseModal();
  useCookieBanner();
  useOrderPopup();
  usePromotionPopup();
  useAuthPopup();
});