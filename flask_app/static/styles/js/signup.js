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
    const confirmPassword = document.getElementById("confirm-password-field");
    const accountType = document.querySelector('input[name="account_type"]:checked').value;

    const firstNameError = document.getElementById("first-name-error");
    const lastNameError = document.getElementById("last-name-error");
    const emailError = document.getElementById("email-error");
    const passwordError = document.getElementById("password-error");
    const confirmPasswordError = document.getElementById("confirm-password-error");

    clearError(firstNameError, lastNameError, emailError, passwordError);

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

    if (valid) {
        event.target.submit();
    }

    if (confirmPassword.value.trim() === "") {
        showError(confirmPassword, "Confirm Password is required", confirmPasswordError);
        valid = false;
    } else if (confirmPassword.value !== password.value) {
        showError(confirmPassword, "Passwords must match", confirmPasswordError);
        valid = false;
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