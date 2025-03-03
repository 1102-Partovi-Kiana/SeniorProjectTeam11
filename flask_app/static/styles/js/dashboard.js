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
    const editButtons = document.querySelectorAll(".edit-button");
    
    editButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent form submission
            const userId = button.closest('form').querySelector('input[name="selected_user_id"]').value;
            const modal = document.getElementById(`edit-modal-${userId}`);
            modal.style.display = "block";
        });
    });

    const closeModals = document.querySelectorAll(".close-modal");
    closeModals.forEach(closeButton => {
        closeButton.addEventListener("click", function () {
            const modal = closeButton.closest('.modal');
            modal.style.display = "none";
        });
    });

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
    const editButtons = document.querySelectorAll(".edit-button");

    editButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent default action
            const classId = button.closest('form').querySelector('input[name="selected_class_id"]').value;
            const modal = document.getElementById(`edit-modal-${classId}`);
            if (modal) {
                modal.style.display = "block";
            }
        });
    });

    const closeModals = document.querySelectorAll(".close-modal");
    closeModals.forEach(closeButton => {
        closeButton.addEventListener("click", function () {
            const modal = closeButton.closest('.modal');
            modal.style.display = "none";
        });
    });

    window.addEventListener("click", function (event) {
        const modals = document.querySelectorAll(".modal");
        modals.forEach(modal => {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        });
    });
});

function openConfirmationModal() {
    document.getElementById('confirmation-modal').style.display = 'flex';
}

function closeConfirmationModal() {
    document.getElementById('confirmation-modal').style.display = 'none';
}

document.querySelector('.close-confirmation-modal').addEventListener('click', closeConfirmationModal);
document.getElementById('cancel-action-button').addEventListener('click', closeConfirmationModal);

document.querySelector('.apply-changes-button').addEventListener('click', function(event) {
    event.preventDefault();
    openConfirmationModal();
    window.pendingForm = event.target.closest('form');
});

document.getElementById('remove-button').addEventListener('click', function(event) {
    event.preventDefault();
    openConfirmationModal();

    window.pendingForm = event.target.closest('form');
});

document.getElementById('confirm-action-button').addEventListener('click', function() {
    if (window.pendingForm) {
        window.pendingForm.submit();
    }
    closeConfirmationModal();
});