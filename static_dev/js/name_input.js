document.addEventListener("DOMContentLoaded", function () {
  const nameInputs = document.querySelectorAll('input[text-name-input]');

  const onNameInput = function (e) {
    const input = e.target;
    input.value = input.value.replace(/[^a-zA-Zа-яА-я- ]/g, '');
  };

  for (const nameInput of nameInputs) {
        nameInput.addEventListener('input', onNameInput, false);
        nameInput.addEventListener('paste', onNameInput, false);
    }
})