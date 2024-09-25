const useInputPhoneMask = () => {
    const phoneInputs = document.querySelectorAll('input[type=tel]');

    const getInputNumbersValue = function (input) {
        // Return stripped input value — just numbers and "+" sign
        return input.value.replace(/[^0-9+]+|(?!^)\+/g, '');
    };

    const formatInput = function (input) {
        let formattedOutput = "+7 ";
        if (input.length > 1) formattedOutput += '(' + input.substring(1, 4);
        if (input.length >= 5) formattedOutput += ') ' + input.substring(4, 7);
        if (input.length >= 8) formattedOutput += '-' + input.substring(7, 9);
        if (input.length >= 10) formattedOutput += '-' + input.substring(9, 11);
        return formattedOutput
    };

    const onPhonePaste = function (e) {
        const input = e.target,
          inputNumbersValue = getInputNumbersValue(input);
        const pasted = e.clipboardData || window.clipboardData;
        if (pasted) {
            const pastedText = pasted.getData('Text');
            if (/[^0-9+]+|(?!^)\+/g.test(pastedText)) {
                // Attempt to paste non-numeric symbol — remove all non-numeric symbols,
                // formatting will be in onPhoneInput handler
                input.value = inputNumbersValue;
            }
        }
    };


    const onPhoneInput = function (e) {
        let input = e.target,
          inputNumbersValue = getInputNumbersValue(input),
          selectionStart = input.selectionStart,
          formattedInputValue = "";

        if (!inputNumbersValue) {
            return input.value = "";
        }

        if (input.value.length !== selectionStart) {
            // Editing in the middle of input, not last symbol
            if (e.data && /\D/g.test(e.data)) {
                // Attempt to input non-numeric symbol
                input.value = inputNumbersValue;
            }
            return;
        }

        let originalInputValue = inputNumbersValue;

        if (inputNumbersValue.includes("+")) {
            // If input value contains "+", then remove it
            inputNumbersValue = inputNumbersValue.replaceAll("+", '')
        }

        if (inputNumbersValue[0] === "7") {
            formattedInputValue = formatInput(inputNumbersValue);

        } else if (["8", "9"].indexOf(inputNumbersValue[0]) > -1 &&
          (originalInputValue.length < 2 || originalInputValue.length > 9)) {

            if (inputNumbersValue[0] === "8") inputNumbersValue = inputNumbersValue.substring(1);

            inputNumbersValue = "7" + inputNumbersValue;
            formattedInputValue = formatInput(inputNumbersValue);

        } else {
            formattedInputValue = "+" + inputNumbersValue.substring(0, 11);
        }

        input.value = formattedInputValue;
    };

    const onPhoneKeyDown = function (e) {
        // Clear input after remove last symbol
        const inputValue = e.target.value.replace(/\D/g, '');
        if (e.keyCode === 8 && inputValue.length === 1) {
            e.target.value = "";
        }
    };
    for (const phoneInput of phoneInputs) {
        phoneInput.addEventListener('keydown', onPhoneKeyDown);
        phoneInput.addEventListener('input', onPhoneInput, false);
        phoneInput.addEventListener('paste', onPhonePaste, false);
    }
};
export {
  useInputPhoneMask as u
};