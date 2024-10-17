import "../utils/modulepreload-polyfill.js";
import { uPP as usePromotionPopup } from "../utils/popups.js";
import { uOP as useOrderPopup } from "../utils/orders.js";
import {
  u as useBurger, a as useHeaderOnScroll, c as useCookieBanner
} from "../utils/base.js";
import { Au as useAuthPopup } from "../utils/auth.js";
import { u as useShowcaseModal } from "../utils/showcase-modal.js";
import { c as  useSingleNewsSlider } from "../utils/sliders.js";



addEventListener("DOMContentLoaded", () => {
  useBurger();
  useHeaderOnScroll(true);
  useCookieBanner();
  usePromotionPopup();
  useShowcaseModal();
  useSingleNewsSlider();
  useOrderPopup();
  useAuthPopup();
});
