import {gC as getCookie, sC as setCookie} from "./base.js";
import {MP as popupMessage, P as Popup} from "./popups.js";


class DropdownMenu {
  constructor(
    input,
    term = 'term=',
    className = 'autocomplete-dropdown',
    endpointAttrName = 'autocomplete-url',
    itemStyle = 'flex',
    debounceTimeout = 300
  ) {
    this.isShown = false;
    this.isChoosen = false;
    this.className = className;
    this.itemStyle = itemStyle;
    this._input = input;
    this._menu = null;
    this._term = term;
    this._endpointAttrName = endpointAttrName;
    this._endpoint = this._getEndpoint();
    this._debounceTimeout = debounceTimeout;

    this._updatePosition = this._updatePosition.bind(this);
    this._debounce = this._debounce.bind(this);
    this.getDropdownMenu = this._debounce(this.getDropdownMenu.bind(this), this._debounceTimeout);
    this.addEventListeners()
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
    if (term) {
      this._createMenu(term);
      this.setVisible();
    } else {
      this.setHidden();
    }
  }

  _createMenu(term) {
    if (!this._menu) this._menu = document.body.appendChild(this._createDiv());
    this._updatePosition();
    this._fetchItems(term).then(data => {
      this._menu.innerHTML = '';
      if (data.length === 0) {
        this._menu.appendChild(this._createDiv(`${this.className}-item`, 'Ничего не найдено'));
      } else {
        data.forEach(item => {
          const menuItem = this._createDiv(`${this.className}-item`, item);
          menuItem.addEventListener('click', () => this._setInputValue(item));
          this._menu.appendChild(menuItem);
        });
      }
    });
  }

  _createDiv(className = this.className, text = '', role = '') {
    const div = document.createElement('div');
    div.className = className;
    div.textContent = text;
    div.setAttribute('role', role);
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

  _getEndpoint() {
    const url = this._input.getAttribute(this._endpointAttrName) || '';
    return `${url}?${this._term}`;
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
  document.querySelectorAll(".city-input").forEach(input => {
    new DropdownMenu(input);
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

