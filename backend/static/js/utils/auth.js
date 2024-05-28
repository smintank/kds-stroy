import { P as Popup, MP as popupMessage } from "./popups.js";

const useAuthPopup = () => {
    const popupAuth = new Popup("#popup-auth");
    popupAuth.setEventListeners();

    const signInButton = document.querySelector("#signIn");
    signInButton.addEventListener("click", () => popupAuth.open());

    const formAuth = document.querySelector("#formAuth");
    formAuth.addEventListener("submit", (e) => {
        e.preventDefault();
        popupAuth.close();
        formAuth.reset();
        popupMessage.open('Вход выполнен!', 'Добро пожаловать!');
    });
};

export { useAuthPopup as Au };