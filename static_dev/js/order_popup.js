$(document).ready(function() {
    $('#checkBox').change(function() {
        const $button = $("#orderButton");
        $button.prop("disabled", !this.checked);
        $button.css("background-color", this.checked ? "#C82027" : "#c89fa1");
        $button.css("cursor", this.checked ? "pointer" : "not-allowed");
    });
});
