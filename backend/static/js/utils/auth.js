import { P as Popup} from "./popups.js";

const useAuthPopup = () => {
    const getLogin = () => {
        const loginButton = document.querySelector("#loginButton");
        const formAuth = document.querySelector("#formAuth");
        formAuth.addEventListener("submit", async function (event) {
            event.preventDefault();

            const formData = new FormData(formAuth);
            loginButton.disabled = true;

            try {
                const response = await fetch(formAuth.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    }
                });
                const data = await response.text();
                const parser = new DOMParser();
                const doc = parser.parseFromString(data, 'text/html');

                const errors = doc.querySelectorAll('.errorlist');

                document.querySelectorAll('.errorlist').forEach((error) => error.remove());

                if (errors.length) {
                    errors.forEach((error, index) => {
                        const correspondingInput = formAuth.querySelectorAll(".popup__form-input")[errors.length];
                        correspondingInput.insertAdjacentHTML('afterend', error.outerHTML);
                    });
                    document.getElementById("id_password").value = '';
                } else {
                    window.location.href = "/";
                }
            } catch (err) {
            } finally {
                loginButton.disabled = false;
            }
        });
    }

    if (document.querySelector("#popup-auth") !== null) {
        const popupAuth = new Popup("#popup-auth");
        const signInButton = document.querySelector("#signIn");

        popupAuth.setEventListeners();
        signInButton.addEventListener("click", () => popupAuth.open());
        getLogin();

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