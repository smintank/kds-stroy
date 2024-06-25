import { P as Popup} from "./popups.js";

const useAuthPopup = () => {
    if (document.querySelector("#popup-auth") !== null) {
        const popupAuth = new Popup("#popup-auth");
        popupAuth.setEventListeners();

        const signInButton = document.querySelector("#signIn");
        signInButton.addEventListener("click", () => popupAuth.open());
    } else if (document.querySelector("#popup-logout") !== null) {
        const popupLogout = new Popup("#popup-logout");
        popupLogout.setEventListeners();

        const logoutButton = document.querySelector("#show_logout_popup");
        logoutButton.addEventListener("click", () => popupLogout.open());

        const logoutCancelButton = document.querySelector("#logoutCancelButton");
        logoutCancelButton.addEventListener("click", () => popupLogout.close());
    }
};

export { useAuthPopup as Au };