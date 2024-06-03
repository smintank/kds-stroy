import "../utils/modulepreload-polyfill.js";
import { u as useBurger, a as useHeaderOnScroll, c as useCookieBanner } from "../utils/base.js";
import { u as useShowcaseModal } from "../utils/showcase-modal.js";
import { u as useInputPhoneMask } from "../utils/input-phone-mask.js";


addEventListener("DOMContentLoaded", () => {
  useBurger();
  useHeaderOnScroll();
  useInputPhoneMask();
  useShowcaseModal();
  useCookieBanner();
});