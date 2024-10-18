function ShowClassID() {
    document.getElementById('classID').classList.remove('d-none');
    document.getElementById('classIDField').setAttribute('required', true);
}

function HideClassID() {
    document.getElementById('classID').classList.add('d-none');
    document.getElementById('classIDField').removeAttribute('required');
}

document.getElementById("signupForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const firstName = document.getElementById("inputFirstName");
    const lastName = document.getElementById("inputLastName");
    const email = document.getElementById("inputEmail");
    const password = document.getElementById("inputPassword");
    const classID = document.getElementById("classIDField");
    const accountType = document.querySelector('input[name="accountType"]:checked').value;
    
    const firstNameError = document.getElementById("firstNameError");
    const lastNameError = document.getElementById("lastNameError");
    const emailError = document.getElementById("emailError");
    const passwordError = document.getElementById("passwordError");
    const classIDError = document.getElementById("classIDError");

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
