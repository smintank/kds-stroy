import "../utils/modulepreload-polyfill.js";
import { uPP as usePromotionPopup
} from "../utils/popups.js";
import { uOP as useOrderPopup } from "../utils/orders.js";
import {
  u as useBurger, a as useHeaderOnScroll, c as useCookieBanner
} from "../utils/base.js";




// const useCustomSelect = () => {
//   document.querySelectorAll(".select").forEach((select) => {
//     let selectCurrent = select.querySelector(".select__current"),
//       selectList = select.querySelector(".select__list"),
//       selectInput = select.querySelector(".select__input"),
//       selectItem = select.querySelectorAll(".select__item");
//     selectCurrent.addEventListener("click", () => {
//       selectList.classList.toggle("select__list--show");
//     });
//     selectItem.forEach((item) => {
//       item.addEventListener("click", () => {
//         let itemValue = item.getAttribute("data-value");
//         let itemText = item.textContent;
//         selectInput.value = itemValue;
//         selectCurrent.textContent = itemText;
//         selectListHide();
//       });
//     });
//     let selectListHide = () => {
//       selectList.classList.remove("select__list--show");
//     };
//     document.addEventListener("mouseup", (e) => {
//       if (!select.contains(e.target))
//         selectListHide();
//     });
//   });
// };


addEventListener("DOMContentLoaded", () => {
  useBurger();
  useHeaderOnScroll();
  useCookieBanner();
  usePromotionPopup();
  useOrderPopup();
});
