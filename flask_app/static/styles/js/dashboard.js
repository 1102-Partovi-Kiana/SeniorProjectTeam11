function toggleSelectAll(group) {
    let checkboxes;
    if (group === 'student'){
        checkboxes = document.querySelectorAll('.student-checkbox');
    } else if (group === 'courses') {
        checkboxes = document.querySelectorAll('.courses-checkbox')
    }

    let selectAllCheckbox;
    if (group === 'student'){
        selectAllCheckbox = document.getElementById('selectAllStudents');
    } else if (group ===  'courses') {
        selectAllCheckbox = document.getElementById('selectAllCourses');
    }
    
    checkboxes.forEach(checkbox => {
        checkbox.checked = selectAllCheckbox.checked;
    });
}

document.addEventListener("DOMContentLoaded", function () {
    var classCodeModal = new bootstrap.Modal(document.getElementById('classCodeModal'), {
        keyboard: false
    });
    classCodeModal.show();
});

document.addEventListener("DOMContentLoaded", function () {
    var classSelect = document.getElementById('class-select-assign');
    var assignUrl = document.getElementById('assign-url').value;
    var tableBody = document.querySelector('.student-list-table tbody');

    tableBody.innerHTML = '<tr><td colspan="3">Please select a class.</td></tr>';

    classSelect.addEventListener('change', function () {
        var selectedOption = classSelect.options[classSelect.selectedIndex];
        var classId = selectedOption.value;

        if (!classId) {
            console.log('No class selected.');
            tableBody.innerHTML = '<tr><td colspan="3">Please select a class.</td></tr>';
            return;
        }

        console.log('Selected class_id:', classId);

        fetch(assignUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                class_id: classId
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Response from Flask:", data);

            tableBody.innerHTML = '';

            if (data.students && data.students.length > 0) {
                data.students.forEach(student => {
                    var row = document.createElement('tr');

                    row.innerHTML = `
                        <td><input type="checkbox" name="student_ids" value="${student.user_id}" class="student-checkbox"></td>
                        <td>${student.first_name} ${student.last_name}</td>
                        <td>${student.email}</td>
                    `;

                    tableBody.appendChild(row);
                });
            } else {
                tableBody.innerHTML = '<tr><td colspan="3">No students enrolled in this class.</td></tr>';
            }
        })
        .catch(error => {
            console.error("Error:", error);
            tableBody.innerHTML = '<tr><td colspan="3">Failed to fetch student data. Please try again later.</td></tr>';
        });
    });
});

const buttons = document.querySelectorAll('.class-details-buttons-container button');
const sections = document.querySelectorAll('.class-details-section');

buttons.forEach(button => {
    button.addEventListener('click', () => {
        buttons.forEach(btn => btn.classList.remove('active'));
        
        button.classList.add('active');

        sections.forEach(section => section.classList.remove('active'));

        const targetId = button.getAttribute('data-target');
        const targetSection = document.getElementById(targetId);
        if (targetSection) {
            targetSection.classList.add('active');
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    // For Create Class Modal
    const createClassButton = document.querySelector(".create-class-modal");
    if (createClassButton) {
        createClassButton.addEventListener("click", function (event) {
            event.preventDefault();
            const modal = document.getElementById("createClassModal");
            modal.style.display = "block";
        });
    }

    const joinClassButton = document.querySelector(".join-class-modal");
    if (joinClassButton) {
        joinClassButton.addEventListener("click", function(event) {
            event.preventDefault();
            const modal = document.getElementById("joinClassModal");
            modal.style.display = "block";
        });
    }

    // For Create Class Code Modal
    const createClassCodeButton = document.querySelector(".create-class-code-modal");
    if (createClassCodeButton) {
        createClassCodeButton.addEventListener("click", function(event) {
            event.preventDefault();
            const modal = document.getElementById("createClassCodeModal");
            modal.style.display = "block";
        });
    }

    // For Assign Course Modal
    const assignCourseButton = document.querySelector(".assign-course-modal");
    if (assignCourseButton) {
        assignCourseButton.addEventListener("click", function (event) {
            event.preventDefault();
            const modal = document.getElementById("assignCourseModal");
            modal.style.display = "block";
        });
    }

    // For Edit User Modals (keeping your existing code)
    const editButtons = document.querySelectorAll(".edit-button");
    editButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            const userId = button.closest('form').querySelector('input[name="selected_user_id"]').value;
            const modal = document.getElementById(`edit-modal-${userId}`);
            modal.style.display = "block";
        });
    });

    // Close modals (works for both create and edit modals)
    const closeModals = document.querySelectorAll(".close-modal, .cancel-button, .ok-button");
    closeModals.forEach(closeButton => {
        closeButton.addEventListener("click", function () {
            const modal = closeButton.closest('.modal');
            modal.style.display = "none";
            const form = modal.querySelector("form");
            if (form) {
                form.reset();
            }
        });
    });

    // Close when clicking outside (works for all modals)
    window.addEventListener("click", function (event) {
        const modals = document.querySelectorAll(".modal");
        modals.forEach(modal => {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    // Function to show the confirmation modal
    function showConfirmationModal(event, form, userId) {
        event.preventDefault(); // Prevent the form from submitting immediately
        const confirmationModal = document.getElementById(`confirmation-modal-${userId}`);
        confirmationModal.style.display = 'block'; // Show the confirmation modal
        confirmationModal.setAttribute('aria-hidden', 'false'); // Improve accessibility

        // Store the form in a data attribute
        confirmationModal.dataset.formToSubmit = form.id;
    }

    // Function to hide the confirmation modal
    function hideConfirmationModal(userId) {
        const confirmationModal = document.getElementById(`confirmation-modal-${userId}`);
        confirmationModal.style.display = 'none';
        confirmationModal.setAttribute('aria-hidden', 'true');
    }

    // Event delegation for "Apply Changes" and "Remove User" buttons
    document.addEventListener('click', function (event) {
        const applyChangesButton = event.target.closest('.apply-changes-button');
        const removeButton = event.target.closest('.remove-button');

        if (applyChangesButton) {
            const userId = applyChangesButton.dataset.userId;
            const form = document.getElementById(`update-user-form-${userId}`);
            showConfirmationModal(event, form, userId);
        }

        if (removeButton) {
            const userId = removeButton.dataset.userId;
            const form = document.getElementById(`remove-user-form-${userId}`);
            showConfirmationModal(event, form, userId);
        }
    });

    // Event delegation for confirmation and cancel buttons
    document.addEventListener('click', function (event) {
        const confirmButton = event.target.closest('.confirm-button');
        const cancelButton = event.target.closest('.cancel-button');
        const closeConfirmationModal = event.target.closest('.close-confirmation-modal');

        if (confirmButton || cancelButton || closeConfirmationModal) {
            const userId = (confirmButton || cancelButton || closeConfirmationModal).dataset.userId;
            const confirmationModal = document.getElementById(`confirmation-modal-${userId}`);

            if (confirmButton) {
                const formId = confirmationModal.dataset.formToSubmit;
                const form = document.getElementById(formId);
                if (form) {
                    form.submit(); // Submit the form
                }
            }

            hideConfirmationModal(userId); // Hide the confirmation modal
        }
    });

    // Close the confirmation modal if the user clicks outside of it
    document.addEventListener('click', function (event) {
        if (event.target.classList.contains('modal')) {
            const userId = event.target.id.replace('confirmation-modal-', '');
            hideConfirmationModal(userId);
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    // Check if completion modal exists on the page
    const completionModal = document.getElementById('courseCompletionModal');
    
    if (completionModal) {
        // Show the modal
        completionModal.style.display = 'block';
        
        // Close modal when clicking the X button
        const closeButton = completionModal.querySelector('.close-modal');
        closeButton.addEventListener('click', function() {
            completionModal.style.display = 'none';
        });
        
        // Close modal when clicking outside
        window.addEventListener('click', function(event) {
            if (event.target === completionModal) {
                completionModal.style.display = 'none';
            }
        });
    }
});