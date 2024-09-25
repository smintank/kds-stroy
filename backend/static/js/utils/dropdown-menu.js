

class DropdownMenu {
  constructor(
    input,
    term = 'term=',
    className = 'autocomplete-dropdown',
    idName = 'item-id',
    endpointAttrName = 'autocomplete-url',
    itemStyle = 'flex',
    debounceTimeout = 300
  ) {
    this.className = className;
    this.idName = idName;
    this.itemStyle = itemStyle;
    this._input = input;
    this._menu = null;
    this._term = term;
    this._endpointAttrName = endpointAttrName;
    this._endpoint = this._getEndpoint();
    this.chosenId = this._getCityId(input);
    this._debounceTimeout = debounceTimeout;

    this._updatePosition = this._updatePosition.bind(this);
    this._debounce = this._debounce.bind(this);
    this.getDropdownMenu = this._debounce(this.getDropdownMenu.bind(this), this._debounceTimeout);
    this.addEventListeners()
  }

  setVisible() {
    if (!this._menu) return;
    this._menu.style.display = this.itemStyle;
  }

  setHidden() {
    if (!this._menu) return;
    this._menu.style.display = 'none';
  }

  getDropdownMenu() {
    this.idName = null;
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
          let [item_key, item_value] = item
          const menuItem = this._createDiv(`${this.className}-item`, item_value);
          menuItem.setAttribute(this.idName, item_key);
          menuItem.addEventListener('click', () => this._setInputValue(item_key, item_value));
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
    if (!this._menu) return;
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

  _setInputValue(id, data) {
    this._input.value = String(data);
    this.setHidden();
    this.chosenId = id;
  }

  _getEndpoint() {
    const url = this._input.getAttribute(this._endpointAttrName) || '/autocomplete/';
    return `${url}?${this._term}`;
  }

  _getCityId(input) {
    const cityId = input.getAttribute('city-id');
    if (cityId) {
      return cityId;
    } else {
      return null;
    }
  }

  addEventListeners () {
    window.addEventListener('resize', this._updatePosition);
    window.addEventListener('scroll', this._updatePosition);
    window.addEventListener('orientationchange', this._updatePosition);
    document.addEventListener('click', function(event) {
      if (this._menu) this._menu.setHidden();
    });
    this._input.addEventListener('input', this.getDropdownMenu)
  }
}

export {
  DropdownMenu as dM
};