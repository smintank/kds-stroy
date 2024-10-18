import "../utils/modulepreload-polyfill.js";
import { uPP as usePromotionPopup } from "../utils/popups.js";
import { uOP as useOrderPopup } from "../utils/orders.js";
import {
  u as useBurger, a as useHeaderOnScroll, c as useCookieBanner
} from "../utils/base.js";
import { Au as useAuthPopup } from "../utils/auth.js";



const useNewsFilter = () => {
  document.querySelectorAll(".select").forEach((select) => {
    let selectCurrent = select.querySelector(".select__current"),
      selectList = select.querySelector(".select__list"),
      selectInput = select.querySelector(".select__input"),
      selectItem = select.querySelectorAll(".select__item");

    // Function to hide the select list
    let selectListHide = () => {
      selectList.classList.remove("select__list--show");
    };

    // Show the select list on current select click
    selectCurrent.addEventListener("click", () => {
      selectList.classList.toggle("select__list--show");
    });

    // Add click event to each select item
    selectItem.forEach((item) => {
      item.addEventListener("click", () => {
        let itemValue = item.getAttribute("data-value");
        let itemText = item.textContent;
        selectInput.value = itemValue;
        selectCurrent.textContent = itemText;
        selectListHide();

        const currentURL = new URL(window.location.href);
        let sortingValue = currentURL.searchParams.get("sorting");
        if (!sortingValue) {
          sortingValue = "newest"; // Default sorting
        }

        let newURL = `${window.location.protocol}//${window.location.hostname}${window.location.port ? `:${window.location.port}` : ''}/news/`;

        if (itemValue === "all") {
          newURL += `?sorting=${encodeURIComponent(sortingValue)}`;
        } else {
          newURL += `?category=${encodeURIComponent(itemValue)}&sorting=${encodeURIComponent(sortingValue)}`;
        }

        window.location.href = newURL;
      });
    });

    // Set the current select text based on the URL parameter on page load
    const currentURL = new URL(window.location.href);
    let categoryValue = currentURL.searchParams.get("category");
    if (categoryValue) {
      let currentItem = select.querySelector(`.select__item[data-value="${categoryValue}"]`);
      if (currentItem) {
        selectCurrent.textContent = currentItem.textContent;
      }
    } else {
      selectCurrent.textContent = "Все новости"; // Default text
    }

    // Hide the select list if clicking outside of it
    document.addEventListener("mouseup", (e) => {
      if (!select.contains(e.target))
        selectListHide();
    });
  });
};

const useNewsSorting = () => {
  const sortButton = document.getElementById("news-sort-date");

  // Function to update the arrow based on the sorting parameter
  const updateArrow = () => {
    const currentURL = new URL(window.location.href);
    const sortingValue = currentURL.searchParams.get("sorting");

    if (sortingValue === "oldest") {
      sortButton.classList.add("rotated");
    } else {
      sortButton.classList.remove("rotated");
    }
  };

  // Initial call to update the arrow on page load
  updateArrow();

  sortButton.addEventListener("click", () => {
    const currentURL = new URL(window.location.href);
    let sortingValue = currentURL.searchParams.get("sorting");
    let categoryValue = currentURL.searchParams.get("category");

    if (sortingValue === "newest" || !sortingValue) {
      sortingValue = "oldest";
    } else {
      sortingValue = "newest";
    }

    let newURL = `${window.location.protocol}//${window.location.hostname}${window.location.port ? `:${window.location.port}` : ''}/news/`;

    if (categoryValue) {
      newURL += `?category=${encodeURIComponent(categoryValue)}&sorting=${encodeURIComponent(sortingValue)}`;
    } else {
      newURL += `?sorting=${encodeURIComponent(sortingValue)}`;
    }

    window.location.href = newURL;
  });
};



addEventListener("DOMContentLoaded", () => {
  useBurger();
  useHeaderOnScroll(true);
  useCookieBanner();
  usePromotionPopup();
  useOrderPopup();
  useNewsFilter();
  useNewsSorting();
  useAuthPopup();
});
