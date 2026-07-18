document.addEventListener("DOMContentLoaded", function () {
    const deliveryDateInput = document.getElementById("deliveryDatePicker");
    const selectedDeliveryDate = document.getElementById("selectedDeliveryDate");

    if (!deliveryDateInput || typeof flatpickr === "undefined") {
        return;
    }

    flatpickr(deliveryDateInput, {
        inline: true,
        minDate: "today",
        dateFormat: "Y-m-d",
        disableMobile: true,

        onChange: function (selectedDates, dateStr, instance) {
            if (selectedDates.length > 0 && selectedDeliveryDate) {
                selectedDeliveryDate.textContent = instance.formatDate(
                    selectedDates[0],
                    "D d M Y"
                );
            }
        }
    });
});