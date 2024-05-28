import { gC as getCookie, sC as setCookie } from "./base.js";
import { P as Popup, MP as popupMessage } from "./popups.js";

let cityChosen = false;
const baseURL = `${window.location.protocol}//${window.location.hostname}:${window.location.port}`;
console.log(baseURL);

const popupOrder = new Popup("#popup-order");
popupOrder.setEventListeners();

const useCitySuggestions = () => {
  const cityField = document.getElementById("id_city");
  let dropdown;

  function updateDropdownPosition() {
    const rect = cityField.getBoundingClientRect();
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const scrollLeft = window.scrollX || document.documentElement.scrollLeft;

    if (dropdown) {
      dropdown.style.position = 'absolute';
      dropdown.style.top = `${rect.bottom + scrollTop}px`;
      dropdown.style.left = `${rect.left + scrollLeft}px`;
      dropdown.style.width = `${rect.width}px`;
    }
  }

  function debounce(func, wait) {
    let timeout;
    return function (...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  function handleAutocomplete(input) {
    const debouncedFetch = debounce(function (event) {
      const term = event.target.value;
      console.log(term);
      if (!term) {
        if (dropdown) dropdown.style.display = 'none';
        return;
      }
      fetch(
        '/orders/autocomplete/location/?term=' + encodeURIComponent(term)
      ).then(
        response => response.json()
      ).then(data => {
        console.log(data);
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

    window.setCity = function (item) {
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
  useCitySuggestions();
};

export {
  useOrderFormWithImages as uOP
};

