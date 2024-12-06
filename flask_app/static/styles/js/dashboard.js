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

