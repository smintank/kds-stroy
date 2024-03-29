import "./modulepreload-polyfill-BoyGcPDr.js";
import { P as Popup, u as useBurger, a as useHeaderOnScroll, PP as PromotionPopup } from "./headerOnScroll-BsQcXGBC.js";
import { u as useShowcaseModal } from "./showcaseModal-BGg2r-Tz.js";
import { u as useProjectsRepairsSlider, a as useProjectsBigsSlider, b as useReviewsSlider } from "./sliders-C0i03PCH.js";
import { u as useInputPhoneMask } from "./useInputPhoneMask-CE77khD0.js";

const popupOrder = new Popup("#popup-order");
  popupOrder.setEventListeners();

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
const useActiveNavSection = () => {
  const navLinks = document.querySelectorAll(".header__nav-list-item a");
  const headerHeight = document.querySelector(".header").offsetHeight;
  window.onscroll = function() {
    navLinks.forEach((navLink) => {
      if (navLink.getAttribute("href") === "#")
        return;
      const section = document.querySelector(navLink.getAttribute("href"));
      if (section.offsetTop - headerHeight <= window.scrollY && section.offsetTop + section.offsetHeight > window.scrollY) {
        navLink.classList.add("header__nav-list-item--active");
      } else {
        navLink.classList.remove("header__nav-list-item--active");
      }
    });
  };
};

const popupSuccess = new Popup("#popup-contacts");
popupSuccess.setEventListeners();
const popupFailure = new Popup("#popup-failure");
popupFailure.setEventListeners();

const useContactsFormWithImages = () => {
  const formData = new FormData();
  let imageNumbers = 0;
  function containsFile(formData2, photoName) {
    return Array.from(formData2.values()).some(
      (photo) => photo.name === photoName
    );
  }
  function addPreviewItem(currentPhotoId, photo) {
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
  document.querySelector("#fileInput").addEventListener("change", (e) => {
    const photos = e.target.files;
    Array.from(photos).forEach((photo) => {
      if (!containsFile(formData, photo.name) && Array.from(formData.entries()).length < 5) {
        const currentPhotoId = "photo-" + imageNumbers;
        addPreviewItem(currentPhotoId, photo);
        formData.append(currentPhotoId, photo);
        imageNumbers++;
      }
    });
    togglePhotoTools(formData);
  });
  document.addEventListener("click", function(e) {
    if (e.target.classList.contains("remove-button")) {
      formData.delete(e.target.getAttribute("image-id"));
      e.target.parentNode.remove();
      togglePhotoTools(formData);
    }
  });
  document.getElementById("orderForm").addEventListener("submit", function(e) {
    e.preventDefault();
    const originFormData = new FormData(this);
    originFormData.delete("photo");
    for (const [key, value] of formData.entries()) {
      originFormData.append(key, value);
    }
    this.reset();
    fetch("/orders/create/", {
      method: "POST",
      body: originFormData
    }).then(function(response) {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("Ошибка при создании заказа!");
      }
    }).then(function(data) {
      popupOrder.close();
      popupSuccess.open();
      setCookie('order_created', true, 1);
      const messageElement = document.querySelector("#successMessage");
      const textElement = document.querySelector("#successText");
        if (messageElement) {
          messageElement.textContent = data.message;
          textElement.textContent = data.text
        }
    }).catch(function(error) {
      popupFailure.open();
      const messageElement = document.querySelector("#failureMessage");
        console.log(error)
        if (messageElement) messageElement.textContent = error;
    });
  });
};
// const useFileInput = () => {
//   const input = document.querySelector("#upload-images");
//   console.log(input);
// };
function setCookie(cname, cvalue, exdays) {
  const d = /* @__PURE__ */ new Date();
  d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1e3);
  const expires = "expires=" + d.toUTCString();
  document.cookie = cname + "=" + cvalue + "; " + expires;
}
function getCookie(cname) {
  const name = cname + "=";
  const ca = document.cookie.split(";");
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == " ")
      c = c.substring(1);
    if (c.indexOf(name) == 0)
      return c.substring(name.length, c.length);
  }
  return false;
}
const useCustomAnchorScroll = () => {
  const headerHeight = document.querySelector(".header").offsetHeight;
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function(e) {
      e.preventDefault();
      const element = document.querySelector(this.getAttribute("href"));
      if (!element)
        return;
      window.scrollTo(0, element.offsetTop - headerHeight);
    });
  });
};
const useWorksToggle = (e) => {
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
  // useFileInput();
  useContactsFormWithImages();
  useCustomAnchorScroll();
  useActiveNavSection();

  const popupNewsSub = new Popup("#popup-news-sub");
  popupNewsSub.setEventListeners();
  const promotionPopup = new PromotionPopup("#popup-promotion");
  promotionPopup.setEventListeners();

  if (getCookie("promo_popup_hide")) promotionPopup.close();
  setCookie("promo_popup_hide", true, 1);

  const formStocks = document.querySelector("#formStocks");
  formStocks.addEventListener("submit", (e) => {
    e.preventDefault();
    formStocks.reset();
    popupNewsSub.open();
  });

  const orderPopupButton = document.querySelectorAll("#orderPopup");
  orderPopupButton.forEach((button) => {
    button.addEventListener("click", () => {
      if (getCookie("order_created") !== "true") {
        popupOrder.open();
      } else {
        console.log("order already created");
        const messageElement = document.querySelector("#successMessage");
        const textElement = document.querySelector("#successText");
        messageElement.textContent = "Вы уже отправили заявку!";
        textElement.textContent = "Мы свяжемся с вами в ближайшее время";
        popupSuccess.open();
      }
    });
  });


  // Auth and Sign In Popups
  // const popupSuccess2 = new Popup("#popup-success");
  // popupSuccess2.setEventListeners();
  // const popupFailure2 = new Popup("#popup-failure");
  // popupFailure2.setEventListeners();
  // const popupAuth = new Popup("#popup-auth");
  // if (popupAuth) {
  //   popupAuth.setEventListeners();
  // }
  // const signInButton = document.querySelector("#signIn");
  // if (signInButton) {
  //   signInButton.addEventListener("click", () => popupAuth.open());
  // }
  // const formAuth = document.querySelector("#formAuth");
  // formAuth.addEventListener("submit", (e) => {
  //   e.preventDefault();
  //   popupAuth.close();
  //   formAuth.reset();
  //   popupSuccess2.open();
  // });
});

document.addEventListener("DOMContentLoaded", function() {
    // Function to show the cookie banner if the user has not accepted cookies
    const cookieBanner = document.getElementById('cookieBanner');
    const acceptedCookies = getCookie('acceptedCookies');
    if (!acceptedCookies) cookieBanner.style.display = 'flex';

    document.getElementById('acceptCookies').addEventListener("click", function() {
        setCookie('acceptedCookies', true, 365); // Expires in 365 days
        cookieBanner.style.display = 'none';
    });
});
