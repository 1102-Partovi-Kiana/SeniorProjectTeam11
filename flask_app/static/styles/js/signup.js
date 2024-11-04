function ShowClassID() {
    document.getElementById('class-id-section').classList.remove('d-none');
    document.getElementById('class-id-input').setAttribute('required', true);
}

function HideClassID() {
    document.getElementById('class-id-section').classList.add('d-none');
    document.getElementById('class-id-input').removeAttribute('required');
}

document.getElementById("signup-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const firstName = document.getElementById("first-name");
    const lastName = document.getElementById("last-name");
    const email = document.getElementById("email-address");
    const password = document.getElementById("password-field");
    const classID = document.getElementById("class-id-input");
    const accountType = document.querySelector('input[name="accountType"]:checked').value;
    
    const firstNameError = document.getElementById("first-name-error");
    const lastNameError = document.getElementById("last-name-error");
    const emailError = document.getElementById("email-error");
    const passwordError = document.getElementById("password-error");
    const classIDError = document.getElementById("class-id-error");

    clearError(firstNameError, lastNameError, emailError, passwordError, classIDError);

    let valid = true;

    if (firstName.value.trim() === "") {
        showError(firstName, "First Name is required", firstNameError);
        valid = false;
    }

    if (lastName.value.trim() === "") {
        showError(lastName, "Last Name is required", lastNameError);
        valid = false;
    }

    if (email.value.trim() === "") {
        showError(email, "Email Address is required", emailError);
        valid = false;
    }

    if (password.value.trim() === "") {
        showError(password, "Password is required", passwordError);
        valid = false;
    }

    if (accountType === "option2" && classID.value.trim() === "") {
        showError(classID, "Class ID is required for students", classIDError);
        valid = false;
    }

    if (valid) {
        event.target.submit();
    }
});

function showError(inputField, message, errorContainer) {
    if (!errorContainer) {
        errorContainer = document.createElement('div');
        errorContainer.style.color = "red";
        errorContainer.style.marginTop = "5px";
        inputField.parentNode.appendChild(errorContainer);
    }
    errorContainer.innerText = message;
}

function clearError(...errorContainers) {
    errorContainers.forEach(function(errorContainer) {
        if (errorContainer) {
            errorContainer.innerText = "";
        }
    });
}