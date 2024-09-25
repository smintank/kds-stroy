const form = document.querySelector('[name="verifyForm"]');
const inputs = form.querySelectorAll('.inputs input');
const formData = new FormData();

function shouldSubmit() {
  return [...inputs].every((input) => input.value.length > 0);
}

function handleSubmit(e) {
  e.preventDefault();

  if (shouldSubmit()) {
    document.querySelector('input[name="pincode"]').value = [...formData.values()].join('');
    form.submit();
  }
}

function handleInput(e) {
  const input = e.target;
  if (input.value) {
    formData.append(input.name, input.value);

    if (input.nextElementSibling) {
      input.nextElementSibling.focus();
    } else {
      handleSubmit(e);
    }
  }
}

function handleFocus(e) {
  if (e.target.value) {
    e.target.select();
  }
}

function handlePaste(e) {
  const paste = e.clipboardData.getData('text');
  inputs.forEach((input, i) => {
    input.value = paste[i] || '';
    formData.set(input.name, input.value);
  })
  if (shouldSubmit()) {
    handleSubmit(e);
  }
}

function handleKeyDown({ key, target }) {
  if (key === 'Backspace' && target.previousElementSibling) {
    formData.delete(target.name);
    target.value = '';
    target.previousElementSibling.focus();
  }
}

function useSmsInput() {
  inputs[0].addEventListener('paste', handlePaste);

  form.addEventListener('input', handleInput);
  form.addEventListener('focusin', handleFocus);
  form.addEventListener('keydown', handleKeyDown);
  form.onsubmit = handleSubmit;
}

export { useSmsInput as SI };