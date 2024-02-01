document.addEventListener("DOMContentLoaded", function () {
    var phoneInputs = document.querySelectorAll('input[data-tel-input]');

    var getInputNumbersValue = function (input) {
        // Return stripped input value — just numbers and "+" sign
        return input.value.replace(/[^0-9+]+|(?!^)\+/g, '');
    }

    var  formatInput = function(input) {
        var formattedOutput = "+7 ";
        if (input.length > 1) formattedOutput += '(' + input.substring(1, 4);
        if (input.length >= 5) formattedOutput += ') ' + input.substring(4, 7);
        if (input.length >= 8) formattedOutput += '-' + input.substring(7, 9);
        if (input.length >= 10) formattedOutput += '-' + input.substring(9, 11);
        return formattedOutput
    }

    var onPhonePaste = function (e) {
        var input = e.target,
            inputNumbersValue = getInputNumbersValue(input);
        var pasted = e.clipboardData || window.clipboardData;
        if (pasted) {
            var pastedText = pasted.getData('Text');
            if (/[^0-9+]+|(?!^)\+/g.test(pastedText)) {
                // Attempt to paste non-numeric symbol — remove all non-numeric symbols,
                // formatting will be in onPhoneInput handler
                input.value = inputNumbersValue;
                return;
            }
        }
    }


    var onPhoneInput = function (e) {
        var input = e.target,
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
            formattedInputValue = "+" + inputNumbersValue.substring(0, 16);
        }

        input.value = formattedInputValue;
    }

    var onPhoneKeyDown = function (e) {
        // Clear input after remove last symbol
        var inputValue = e.target.value.replace(/\D/g, '');
        if (e.keyCode == 8 && inputValue.length == 1) {
            e.target.value = "";
        }
    }
    for (var phoneInput of phoneInputs) {
        phoneInput.addEventListener('keydown', onPhoneKeyDown);
        phoneInput.addEventListener('input', onPhoneInput, false);
        phoneInput.addEventListener('paste', onPhonePaste, false);
    }
})
