document.addEventListener("DOMContentLoaded", function () {
    const profileForm = document.getElementById("profileForm");
    const editButton = document.getElementById("editProfileBtn");
    const saveButton = document.getElementById("saveProfileBtn");

    if (!profileForm || !editButton || !saveButton) {
        return;
    }

    const fields = profileForm.querySelectorAll("input, textarea, select");

    function lockFields() {
        fields.forEach(function (field) {
            if (field.tagName === "SELECT") {
                field.disabled = true;
            } else {
                field.readOnly = true;
            }

            field.classList.add("profile-field-locked");
            field.classList.remove("profile-field-editing");
        });

        saveButton.disabled = true;
    }

    function unlockFields() {
        fields.forEach(function (field) {
            if (field.tagName === "SELECT") {
                field.disabled = false;
            } else {
                field.readOnly = false;
            }

            field.classList.remove("profile-field-locked");
            field.classList.add("profile-field-editing");
        });

        saveButton.disabled = false;
    }

    lockFields();

    editButton.addEventListener("click", function () {
        unlockFields();
    });
});