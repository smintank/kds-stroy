import { P as Popup} from "./popups.js";

const useAuthPopup = () => {
    if (document.querySelector("#popup-auth") !== null) {
        const popupAuth = new Popup("#popup-auth");
        const signInButton = document.querySelector("#signIn");
        const formAuth = document.querySelector("#formAuth");

        popupAuth.setEventListeners();
        signInButton.addEventListener("click", () => popupAuth.open());

    } else if (document.querySelector("#popup-logout") !== null) {
        const popupLogout = new Popup("#popup-logout");
        const logoutButton = document.querySelector("#show_logout_popup");
        const logoutCancelButton = document.querySelector("#logoutCancelButton");

        popupLogout.setEventListeners();
        logoutButton.addEventListener("click", () => popupLogout.open());
        logoutCancelButton.addEventListener("click", () => popupLogout.close());
    }
};


export { useAuthPopup as Au };