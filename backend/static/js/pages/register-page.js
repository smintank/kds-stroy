import "../utils/modulepreload-polyfill.js";
import { u as useBurger, a as useHeaderOnScroll } from "../utils/base.js";
import { u as useInputPhoneMask } from "../utils/input-phone-mask.js";


addEventListener("DOMContentLoaded", () => {
  useBurger();
  useHeaderOnScroll(true);
  useInputPhoneMask();
});
