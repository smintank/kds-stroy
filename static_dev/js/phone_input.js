document.addEventListener("DOMContentLoaded", function () {
    var phoneInputs = document.querySelectorAll('input[data-tel-input]');

    var getInputNumbersValue = function (input) {
        // Return stripped input value — just numbers
        return input.value.replace(/[^0-9+]/g, '');
    }

    var onPhonePaste = function (e) {
        var input = e.target,
            inputNumbersValue = getInputNumbersValue(input);
        var pasted = e.clipboardData || window.clipboardData;
        if (pasted) {
            var pastedText = pasted.getData('Text');
            if (/\D/g.test(pastedText)) {
                // Attempt to paste non-numeric symbol — remove all non-numeric symbols,
                // formatting will be in onPhoneInput handler
                input.value = inputNumbersValue;
                return;
            }
        }
    }

    var  inputFormat = function(input, formattedOutput) {
        formattedOutput = input.value = "+7 ";
        if (input.length > 1) formattedOutput += '(' + input.substring(1, 4);
        if (input.length >= 5) formattedOutput += ') ' + input.substring(4, 7);
        if (input.length >= 8) formattedOutput += '-' + input.substring(7, 9);
        if (input.length >= 10) formattedOutput += '-' + input.substring(9, 11);
        return formattedOutput
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


        console.log("First input value: " + inputNumbersValue[0])
        if (inputNumbersValue[0] === "+") {
            // If first symbol is "+", then remove it and show it in input field
            inputNumbersValue = inputNumbersValue.substring(1);
            formattedInputValue = input.value = "+";
        }

        if (inputNumbersValue.includes("+")) {
            // If input value contains "+" more, then remove it
            inputNumbersValue = inputNumbersValue.replace("+", '')
        }

        if (inputNumbersValue[0] === "7") {
            formattedInputValue = inputFormat(inputNumbersValue, formattedInputValue);
        } else if (inputNumbersValue[0] === "8") {
            inputNumbersValue = "7" + inputNumbersValue.substring(1);
            formattedInputValue = inputFormat(inputNumbersValue, formattedInputValue);
        } else if (inputNumbersValue[0] === "9") {
            inputNumbersValue = "7" + inputNumbersValue;
            formattedInputValue = inputFormat(inputNumbersValue, formattedInputValue);
        } else {
            formattedInputValue = "+" + inputNumbersValue.substring(0, 16);
        }

        console.log("Full input value: " + inputNumbersValue)
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
