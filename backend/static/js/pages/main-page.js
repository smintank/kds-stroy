import "../utils/modulepreload-polyfill.js";
import { uPP as usePromotionPopup, M as MessagePopup } from "../utils/popups.js";
import { u as useBurger, a as useHeaderOnScroll, gC as getCookie, sC as setCookie,
        c as useCookieBanner} from "../utils/base.js";
import { uOP as useOrderPopup} from "../utils/orders.js";
import { u as useShowcaseModal } from "../utils/showcase-modal.js";
import { u as useProjectsRepairsSlider, a as useProjectsBigsSlider, b as useReviewsSlider } from "../utils/sliders.js";
import { u as useInputPhoneMask } from "../utils/input-phone-mask.js";
import { Au as useAuthPopup } from "../utils/auth.js";


const useEmailSubscription = () => {
  const popupNewsSub = new MessagePopup("#popup-news-sub");
  popupNewsSub.setEventListeners();
  const emailSubscribed = getCookie('email_subscribed');
    if (emailSubscribed) {
        document.getElementById('stocksFormContainer').style.display = 'none';
    }

  const emailForm = document.querySelector("#formStocks");
  emailForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const stocksFormContainer = document.querySelector("#stocksFormContainer");
    fetch("/subs/subscribe/", {
      method: 'POST',
      body: new FormData(e.target),
      headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
      }
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
      popupNewsSub.open('Ошибка при попытке подписаться!', 'Не удалось подписаться, попробуйте позже! ');
    });
  });
};

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
        scrollOffset = 80;
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

const useActiveNavSection = () => {
  const navLinks = document.querySelectorAll(".header__nav-list-item a");
  const headerHeight = document.querySelector(".header").offsetHeight;

  window.onscroll = function() {
    navLinks.forEach((navLink) => {
      const href = navLink.getAttribute("href");
      if (!href.startsWith('#')) return;

      const section = document.querySelector(href);
      if (section) {
        if (section.offsetTop - headerHeight <= window.scrollY && section.offsetTop + section.offsetHeight > window.scrollY) {
          navLink.classList.add("header__nav-list-item--active");
        } else {
          navLink.classList.remove("header__nav-list-item--active");
        }
      }
    });
  };
};


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
  useOrderPopup();
  useCustomAnchorScroll();
  useActiveNavSection();
  useCookieBanner();
  useEmailSubscription();
  usePromotionPopup();
  useAuthPopup();
});




