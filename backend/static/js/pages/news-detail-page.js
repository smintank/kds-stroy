import "../utils/modulepreload-polyfill.js";
import { uOP as useOrderPopup } from "../utils/orders.js";
import {
  u as useBurger, a as useHeaderOnScroll, c as useCookieBanner
} from "../utils/base.js";
import { c as useSingleNewsSlider } from "../utils/sliders.js";
import {uPP as usePromotionPopup} from "../utils/popups.js";

addEventListener("DOMContentLoaded", () => {
  useBurger();
  useHeaderOnScroll();
  useSingleNewsSlider();
  useCookieBanner();
  usePromotionPopup();
  useOrderPopup();
});
