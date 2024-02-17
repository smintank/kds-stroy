document.addEventListener("DOMContentLoaded", function () {
    var nameInputs = document.querySelectorAll('input[text-name-input]');

    var onNameInput = function (e) {
        var input = e.target
        input.value = input.value.replace(/[^a-zA-Zа-яА-я- ]/g, '');
    }

     for (var nameInput of nameInputs) {
        nameInput.addEventListener('input', onNameInput, false);
        nameInput.addEventListener('paste', onNameInput, false);
    }
})