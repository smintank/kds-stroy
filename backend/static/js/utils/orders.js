import {gC as getCookie, sC as setCookie} from "./base.js";
import {MP as popupMessage, P as Popup} from "./popups.js";


class DropdownMenu {
  constructor(input, endpoint) {
    this.isShown = false;
    this.isChoosen = false;
    this._endpoint = endpoint;
    this._input = input;
    this.className = 'autocomplete-dropdown';
    this.itemStyle = 'flex';
    this._debounceTimeout = 300;
    this._menu = null;

    this._updatePosition = this._updatePosition.bind(this);
    this._debounce = this._debounce.bind(this);
    this.getDropdownMenu = this._debounce(this.getDropdownMenu.bind(this), this._debounceTimeout);
  }

  setVisible() {
    this._menu.style.display = this.itemStyle;
    this.isShown = true;
  }

  setHidden() {
    this._menu.style.display = 'none';
    this.isShown = false;
  }

  getDropdownMenu() {
    this.isChoosen = false;
    const term = this._input.value;
    if (!term) {
      this.setHidden();
      return;
    }
    this._createMenu(term);
  }

  _createMenu(term) {
    if (!this._menu) {
      this._menu = document.body.appendChild(this._createMenuHTML());
    }
    this._updatePosition();
    this._fetchItems(term).then(data => {
      this._menu.innerHTML = '';
      data.forEach(item => {
        const menuItem = this._createMenuItemHTML(item);
        menuItem.addEventListener('click', () => this._setInputValue(item));
        this._menu.appendChild(menuItem);
      });
      if (data.length === 0) {
        this._menu.appendChild(this._createMenuItemHTML('Ничего не найдено'));
      }
      this.setVisible();
    });
  }

  _createMenuHTML() {
    const div = document.createElement('div');
    div.className = this.className;
    div.textContent = '';
    div.setAttribute('role', 'menu');
    return div;
  }

  _createMenuItemHTML(item, onClickFunc) {
    const div = document.createElement('div');
    div.className = `${this.className}-item`;
    div.textContent = item;
    div.setAttribute('role', 'menuitem');
    return div;
  }

  _updatePosition() {
    if (this._menu === '') return;
    const rect = this._input.getBoundingClientRect();
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const scrollLeft = window.scrollX || document.documentElement.scrollLeft;

    this._menu.style.position = 'absolute';
    this._menu.style.top = `${rect.bottom + scrollTop}px`;
    this._menu.style.left = `${rect.left + scrollLeft}px`;
    this._menu.style.width = `${rect.width}px`;
  }

  _debounce(func, wait) {
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

  async _fetchItems(term) {
    try {
      const response = await fetch(this._endpoint + encodeURIComponent(term));
      return await response.json();
    } catch (error) {
      console.error('Error fetching autocomplete suggestions:', error);
      return [];
    }
  }

  _setInputValue(data) {
    this._input.value = String(data);
    this.setHidden();
    this.isChoosen = true;
  }

  addEventListeners () {
    window.addEventListener('resize', this._updatePosition);
    window.addEventListener('scroll', this._updatePosition);
    window.addEventListener('orientationchange', this._updatePosition);
    document.addEventListener('click', function(event) {
      // if (event.target.closest(`#${this.className}, #${this._input.id}`)) return;
      if (this._menu) this._menu.setHidden();
    });
    this._input.addEventListener('input', this.getDropdownMenu)
  }
}

const useCitySuggestions = () => {
  const endpoint = '/orders/autocomplete/location/?term='
  const inputs = document.querySelectorAll('[data-autocomplete-url]');
  inputs.forEach(input => {
    const dropdown = new DropdownMenu(input, endpoint);
    dropdown.addEventListeners()
  });
}


const useOrderFormWithImages = () => {
  const popupOrder = new Popup("#popup-order");
  popupOrder.setEventListeners();
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

