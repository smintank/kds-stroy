import "./modulepreload-polyfill-BoyGcPDr.js";
import { P as Popup, MP as MessagePopup, u as useBurger, a as useHeaderOnScroll,
  PP as PromotionPopup, s as setCookie, g as getCookie, c as useCookieBanner,
  n as useActiveNavSection
} from "./headerOnScroll-BsQcXGBC.js";
import { u as useShowcaseModal } from "./showcaseModal-BGg2r-Tz.js";
import { u as useProjectsRepairsSlider, a as useProjectsBigsSlider, b as useReviewsSlider } from "./sliders-C0i03PCH.js";
import { u as useInputPhoneMask } from "./useInputPhoneMask-CE77khD0.js";

const popupOrder = new Popup("#popup-order");
const popupNewsSub = new MessagePopup("#popup-news-sub");
const popupMessage = new MessagePopup("#popup-message");
const promotionPopup = new PromotionPopup("#popup-promotion");

popupOrder.setEventListeners();
popupNewsSub.setEventListeners();
promotionPopup.setEventListeners();
popupMessage.setEventListeners();

let cityChosen = false;


const useAccordion = () => {
  const accordion = document.querySelector(".accordion");
  const accordionItems = accordion.querySelectorAll(
    ".accordion__list-item-btn"
  );
  accordionItems.forEach((item) => {
    item.addEventListener("click", () => {
      const panel = item.nextElementSibling;
      if (panel.style.maxHeight) {
        panel.style.maxHeight = null;
      } else {
        panel.style.maxHeight = panel.scrollHeight + "px";
      }
      item.classList.toggle("accordion__list-item-btn--active");
    });
  });
};

const useCustomAnchorScroll = () => {
  document.querySelectorAll('.hero__footer-list-item-link, a[href^="#works-section"]').forEach((anchor) => {
    anchor.addEventListener("click", function(e) {
      e.preventDefault();
      let scrollOffset
      const element = document.querySelector(this.getAttribute("href"));
      if (!element)
        return;
      if (this.getAttribute("class") === "hero__footer-list-item-link") {
        scrollOffset = 114;
      } else if (window.innerWidth < 639) {
        scrollOffset = 60;
      } else {
        scrollOffset = 84;
      }
      window.scrollTo(0, element.offsetTop - scrollOffset);
    });
  });
};

const useWorksToggle = () => {
  const links = document.querySelectorAll(".hero__footer-list-item-link");
  const works = document.querySelectorAll(".works__list-item");
  links.forEach((elem) => {
    elem.addEventListener("click", (e2) => {
      links.forEach((elem2) => {
        elem2.parentNode.classList.remove("hero__footer-list-item--active");
      });
      elem.parentNode.classList.add("hero__footer-list-item--active");
      let activeWork;
      works.forEach((elem2) => {
        elem2.classList.remove("works__list-item--active");
        if (`${elem2.id}-link` === e2.target.id) {
          activeWork = elem2;
        }
      });
      activeWork.classList.add("works__list-item--active");
    });
  });
};

const useEmailSubscription = () => {
  const emailSubscribed = getCookie('email_subscribed');
    if (emailSubscribed) {
        document.getElementById('stocksFormContainer').style.display = 'none';
    }

  const emailForm = document.querySelector("#formStocks");
  emailForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const stocksFormContainer = document.querySelector("#stocksFormContainer");
    fetch("/subs/subscribe/", {
      method: "POST",
      body: new FormData(e.target),
    }).then(function(response) {
      if (response.ok) {
        stocksFormContainer.innerHTML = '' +
          '<h2 class="popup__title">Мы рады, что вы с нами!</h2>\n' +
          '<p class="popup__text">\n' +
          'Теперь вы всегда будете в курсе наших новостей, акций и специальных предложений.\n' +
          '</p>';
        setCookie('email_subscribed', true, 1);
      } else {
        throw new Error(response.statusText);
      }
    }).catch(function(error) {
      popupMessage.open('Ошибка при создании заказа!', 'Не удалось подписаться, попробуйте позже!');
    });
  });
};

const usePromotionPopup = () => {
    if (getCookie("promo_popup_hide") === 'true') {
    promotionPopup.close();
  } else {
    promotionPopup.open();
  }
};


const useOrderFormWithImages = () => {
  const formData = new FormData();
  let imageNumbers = 0;

  function togglePhotoTools(formData2) {
    const formDataLength = Array.from(formData2.entries()).length;
    const addImage = document.querySelector("#addImage");
    const addImageText = document.querySelector("#addImageText");
    if (formDataLength < 5) {
      addImage.style.display = "block";
    } else {
      addImage.style.display = "none";
    }
    if (formDataLength <= 0) {
      addImageText.style.display = "block";
    } else {
      addImageText.style.display = "none";
    }
  }

  function addPreviewItem(currentPhotoId, photo) {
    // Add a preview item to the imagePreviews container
    const reader = new FileReader();
    reader.onload = function(event) {
      const imageSrc = event.target.result;
      const element = document.createElement("div");
      element.innerHTML = `
				<div class="preview-image">
					<img alt="uploaded_image" src="${imageSrc}">
					<div class="remove-button" image-id="${currentPhotoId}">&times;</div>
				</div>`;
      document.querySelector("#imagePreviews").append(element);
    };
    reader.readAsDataURL(photo);
  }

  function handleFileInputChange(e) {
    const photos = e.target.files;

    Array.from(photos).forEach((photo) => {
      if (Array.from(formData.entries()).length < 5) {
        const currentPhotoId = "photo-" + imageNumbers;
        addPreviewItem(currentPhotoId, photo);
        formData.append(currentPhotoId, photo);
        imageNumbers++;
      }
    });
    togglePhotoTools(formData);
  }

  document.querySelector("#fileInput").addEventListener("change", handleFileInputChange);

  document.addEventListener("click", function(e) {
    if (e.target.classList.contains("remove-button")) {
      formData.delete(e.target.getAttribute("image-id"));
      e.target.parentNode.remove();
      togglePhotoTools(formData);
    }
  });

  document.getElementById("orderForm").addEventListener("submit", function(e) {
    e.preventDefault();
    popupOrder.close();
    popupMessage.open('Ожидайте...', 'Ваша заявка обрабатывается');

    const originFormData = new FormData(this);
    originFormData.delete("photo");
    for (const [key, value] of formData.entries()) {
      originFormData.append(key, value);
    }
    if (!cityChosen) {
       originFormData.delete("city");
    }

    this.reset();
    fetch("/orders/create/", {
      method: "POST",
      body: originFormData
    }).then(function(response) {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error(response.statusText);
      }
    }).then(function(data) {
      setCookie('order_created', 1, 1);
      setCookie('order_id', data.order_id, 1);
      popupMessage.update(data.message, data.text);
    }).catch(function(error) {
      console.log(error);
      popupMessage.update('Ошибка при создании заказа!', 'Попробуйте позже или свяжитесь с нами');
    });
  });

  document.querySelectorAll("#orderPopup").forEach((button) => {
    button.addEventListener("click", () => {
      if (getCookie("order_created") !== "1") {
        popupOrder.open();
      } else {
        popupMessage.open(
          "Вы уже отправили заявку №" + getCookie("order_id") + "!",
          "Мы свяжемся с вами в ближайшее время"
        );
      }
    });
  });

};

const useCitySuggestions = () => {
  const cityField = document.getElementById("id_city");
  let dropdown;

  function updateDropdownPosition() {
    const rect = cityField.getBoundingClientRect();
    if (dropdown) {
      dropdown.style.top = `${rect.bottom}px`;
      dropdown.style.left = `${rect.left}px`;
      dropdown.style.width = `${rect.width}px`;
    }
  }

  function debounce(func, wait) {
    let timeout;
    return function(...args) {
      const later = () => {
        clearTimeout(timeout);
        updateDropdownPosition();
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  function handleAutocomplete(input) {
    const debouncedFetch = debounce(function(event) {
      const term = event.target.value;
      if (!term) {
        if (dropdown) dropdown.style.display = 'none';
        return;
      }
      fetch(
        'orders/autocomplete/location/?term=' + encodeURIComponent(term)
        ).then(
          response => response.json()
        ).then(data => {
          if (!dropdown) {
            dropdown = document.createElement('div');
            dropdown.id = 'autocomplete-dropdown';
            dropdown.classList.add('autocomplete-dropdown');
            document.body.appendChild(dropdown);
            updateDropdownPosition();
          }
          dropdown.innerHTML = data.map(item => `
            <div class="autocomplete-dropdown-item" onclick="setCity('${item}')">
              ${item}
            </div>
          `).join('') || '<div class="autocomplete-dropdown-item">Ничего не найдено</div>';
          dropdown.style.display = 'flex';
        }).catch(error => {
          console.error('Error fetching autocomplete suggestions:', error);
        });
    }, 300);

    window.setCity = function(item) {
      cityField.value = item;
      dropdown.style.display = 'none';
      cityChosen = true;
    };

    input.addEventListener('input', debouncedFetch);
  }

  const inputs = document.querySelectorAll('[data-autocomplete-url]');
  inputs.forEach(input => handleAutocomplete(input));

  function addEventListeners() {
    window.addEventListener('resize', updateDropdownPosition);
    window.addEventListener('scroll', updateDropdownPosition);
    window.addEventListener('orientationchange', updateDropdownPosition);
  }

  document.addEventListener('click', function(event) {
    if (event.target.closest("#id_city, #autocomplete-dropdown")) return;
    if (dropdown) dropdown.style.display = 'none';
  });

  addEventListeners();
};

const useAuthPopup = () => {
  const popupAuth = new Popup("#popup-auth");
  popupAuth.setEventListeners();

  const signInButton = document.querySelector("#signIn");
  signInButton.addEventListener("click", () => popupAuth.open());

  const formAuth = document.querySelector("#formAuth");
  formAuth.addEventListener("submit", (e) => {
    e.preventDefault();
    popupAuth.close();
    formAuth.reset();
    popupMessage.open('Вход выполнен!', 'Добро пожаловать!');
  });
}


addEventListener("DOMContentLoaded", () => {
  useBurger();
  useHeaderOnScroll();
  useProjectsRepairsSlider();
  useProjectsBigsSlider();
  useReviewsSlider();
  useAccordion();
  useInputPhoneMask();
  useWorksToggle();
  useShowcaseModal();
  useOrderFormWithImages();
  useCustomAnchorScroll();
  useActiveNavSection();
  useCookieBanner();
  useCitySuggestions();
  useEmailSubscription();
  usePromotionPopup();
  // useAuthPopup();
});




