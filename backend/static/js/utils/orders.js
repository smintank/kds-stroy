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
    this._createMenu = this._debounce(this._createMenu.bind(this), this._debounceTimeout);
  }

  setVisible() {
    this._menu.style.display = this.itemStyle;
    this.isShown = true;
  }

  setHidden() {
    this._menu.style.display = 'none'
    this.isShown = false;
  }

  getDropdownMenu() {
    this.isChoosen = false;
    return (event) => {
      const term = event.target.value;
      if (!term) {
        this.setHidden();
        return;
      }
      this._createMenu(term);
    };
  }

  _createMenu(term) {
    if (!this._menu) this._createMenuHTML();
    this._fetchItems(term).then(data => {
      this._menu.innerHTML = '';
      data.forEach(item => {
        this._createMenuItemHTML(this.className + '-item', item, this._setInputValue.bind(this));
      });
      if (data.length === 0) {
        const item = 'Ничего не найдено';
        this._createMenuItemHTML(this.className + '-item', item);
      }
      this.setVisible();
    });
  }

  _createMenuHTML() {
    this._menu = document.createElement('div');
    this._menu.id = this.className;
    this._menu.classList.add(this.className);
    document.body.appendChild(this._menu);
    this._updatePosition();
  }

  _createMenuItemHTML(className, item, onClickFunc) {
    const div = document.createElement('div');
    div.className = 'autocomplete-dropdown-item';
    div.textContent = item;
    if (onClickFunc) div.onclick = () => onClickFunc(item);
    this._menu.appendChild(div);
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
    window.addEventListener('resize', this._menu._updatePosition);
    window.addEventListener('scroll', this._menu._updatePosition);
    window.addEventListener('orientationchange', this._menu._updatePosition);
    document.addEventListener('click', function(event) {
      if (event.target.closest(`#${this.className}, #${this._input.id}`)) return;
      if (this._menu) this._menu.setHidden();
    });
    this._input._addEventListener('input', this.getDropdownMenu())
  }
}

const useInputSuggestions = () => {
  const endpoint = '/orders/autocomplete/location/?term='
  const inputs = document.querySelectorAll('[data-autocomplete-url]');
  inputs.forEach(input => {
    const dropdown = DropdownMenu(input, endpoint);
    dropdown.addEventListeners()
  });
}


const useCitySuggestions = () => {
  function updateDropdownPosition(input) {
    const dropdown = input.dropdown
    if (!input || !dropdown) return;
    const rect = input.getBoundingClientRect();
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const scrollLeft = window.scrollX || document.documentElement.scrollLeft;

    dropdown.style.position = 'absolute';
    dropdown.style.top = `${rect.bottom + scrollTop}px`;
    dropdown.style.left = `${rect.left + scrollLeft}px`;
    dropdown.style.width = `${rect.width}px`;
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
    input.dropdown = null; // Initialize dropdown as a property of the input element

    const debouncedFetch = debounce(function (event) {
      const term = event.target.value;
      if (!term) {
        if (input.dropdown) input.dropdown.style.display = 'none';
        return;
      }
      fetch(
        '/orders/autocomplete/location/?term=' + encodeURIComponent(term)
      ).then(
        response => response.json()
      ).then(data => {
        if (!input.dropdown) {
          input.dropdown = document.createElement('div');
          input.dropdown.id = 'autocomplete-dropdown';
          input.dropdown.classList.add('autocomplete-dropdown');
          document.body.appendChild(input.dropdown);
          updateDropdownPosition(input);
        }
        input.dropdown.innerHTML = '';
        data.forEach(item => {
          const div = document.createElement('div');
          div.className = 'autocomplete-dropdown-item';
          div.textContent = item;
          div.onclick = () => setCity(item, input);
          input.dropdown.appendChild(div);
        });
        if (data.length === 0) {
          const div = document.createElement('div');
          div.className = 'autocomplete-dropdown-item';
          div.textContent = 'Ничего не найдено';
          input.dropdown.appendChild(div);
        }
        input.dropdown.style.display = 'flex';
      }).catch(error => {
        console.error('Error fetching autocomplete suggestions:', error);
      });
    }, 300);

    window.setCity = function (item, cityInput) {
      const dropdown = cityInput.dropdown;
      cityInput.value = item;
      if (dropdown) dropdown.style.display = 'none';
    };

    input.addEventListener('input', debouncedFetch);
  }

  const inputs = document.querySelectorAll('[data-autocomplete-url]');
  inputs.forEach(input => {
    window.addEventListener('resize', updateDropdownPosition.bind(null, input));
    window.addEventListener('scroll', updateDropdownPosition.bind(null, input));
    window.addEventListener('orientationchange', updateDropdownPosition.bind(null, input));
    document.addEventListener('click', function(event) {
      if (event.target.closest("#id_city, #autocomplete-dropdown")) return;
      if (input.dropdown) input.dropdown.style.display = 'none';
    });
    handleAutocomplete(input);
  });
};

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

