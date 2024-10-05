import "../utils/modulepreload-polyfill.js";
import { u as useBurger, a as useHeaderOnScroll, uCS as useCitySuggestions} from "../utils/base.js";
import { u as useShowcaseModal } from "../utils/showcase-modal.js";
import { u as useInputPhoneMask } from "../utils/input-phone-mask.js";
import { uOP as useOrderPopup} from "../utils/orders.js";
import { Au as useAuthPopup } from "../utils/auth.js";
import { uPP as usePromotionPopup } from "../utils/popups.js";

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

const useButtonDisable = () => {
  const form = document.getElementById('accountForm');
  const submitButton = document.getElementById('profileFormSaveButton');
  const initialFormState = new FormData(form);

  function isFormChanged() {
    const currentFormState = new FormData(form);
    for (let [key, value] of initialFormState.entries()) {
      if (currentFormState.get(key) !== value) {
        return true;
      }
    }
    return false;
  }

  function toggleButtonState(isChanged) {
    const baseClass = 'account__form-button-save';
    const disabledClass = `${baseClass}--disabled`;

    if (isChanged) {
      submitButton.disabled = false;
      submitButton.classList.remove(disabledClass);
      submitButton.classList.add(baseClass);

    } else {
      submitButton.disabled = true;
      submitButton.classList.remove(baseClass);
      submitButton.classList.add(disabledClass);
    }
  }

    // Listen for changes in the form
  form.addEventListener('input', function () {
      toggleButtonState(isFormChanged());
  });

  // Listen for select field changes (if any)
  form.addEventListener('change', function () {
      toggleButtonState(isFormChanged());
  });
}

addEventListener("DOMContentLoaded", () => {
  useBurger();
  useHeaderOnScroll();
  useOrderPopup();
  useInputPhoneMask();
  useAccountItem();
  useShowcaseModal();
  useAuthPopup();
  useCitySuggestions();
  useButtonDisable();
  usePromotionPopup();
});
