function filterTableStudents() {
    let nameSearch = document.getElementById("students-search").value.toLowerCase();
    let statusSearch = document.getElementById("status-search").value.toLowerCase();
    let gradeSearch = document.getElementById("grade-search").value.toLowerCase();
    let timeSearch = document.getElementById("time-search").value.toLowerCase();

    const table = document.querySelector(".user-list-table");
    const rows = table.getElementsByTagName("tbody")[0].getElementsByTagName("tr");

    for (let i = 1; i < rows.length; i++) {
        const row = rows[i];
        const cells = row.getElementsByTagName("td");
        
        const nameCell = cells[0]?.textContent.toLowerCase() || "";
        const statusCell = cells[1]?.textContent.toLowerCase() || "";
        const gradeCell = cells[2]?.textContent.toLowerCase() || "";
        const timeCell = cells[3]?.textContent.toLowerCase() || "";

        const nameMatch = nameCell.includes(nameSearch);
        const statusMatch = statusCell.includes(statusSearch);
        const gradeMatch = gradeCell.includes(gradeSearch);
        const timeMatch = timeCell.includes(timeSearch);

        row.style.display = (nameMatch && statusMatch && gradeMatch && timeMatch) ? "" : "none";
    }
}

/* Gradebook Student Loading */

function loadClassStudents(classId) {
    const tbody = document.getElementById('students-table-body');
    
    if (!classId) {
        tbody.innerHTML = '<tr><td colspan="5">Please select a class</td></tr>';
        return;
    }

    tbody.innerHTML = '<tr><td colspan="5" class="loading">Loading students...</td></tr>';

    fetch(`/api/class/${classId}/students`)
        .then(response => {
            if (!response.ok) throw new Error('Failed to load students');
            return response.json();
        })
        .then(data => {
            if (data.students.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5">No students in this class</td></tr>';
                return;
            }

            // Create the filter input row
            const filterRow = `
                <tr>
                    <td>
                        <input type="text" id="students-search" placeholder="Search by Name" oninput="filterTableStudents()">
                    </td>
                    <td>
                        <input type="text" id="status-search" placeholder="Search by Status" oninput="filterTableStudents()">
                    </td>
                    <td>
                        <input type="text" id="grade-search" placeholder="Search by Grade" oninput="filterTableStudents()">
                    </td>
                    <td>
                        <input type="text" id="time-search" placeholder="Search by Time" oninput="filterTableStudents()">
                    </td>
                    <td></td>
                </tr>
            `;

            // Generate student rows
            const studentRows = data.students.map(student => `
                <tr>
                    <td>${student.first_name} ${student.last_name}</td>
                    <td>Active</td>
                    <td>${student.grade}</td>
                    <td>N/A</td>
                    <td>
                        <a href="/dashboard/instructor-view/student-code-log/student-id-${student.user_id}">View Details</a>
                    </td>
                </tr>
            `).join('');

            // Add filter row + student rows
            tbody.innerHTML = filterRow + studentRows;

        })
        .catch(error => {
            console.error('Error:', error);
            tbody.innerHTML = '<tr><td colspan="5">Error loading students</td></tr>';
        });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    const classSelect = document.getElementById('class-select-students');
    classSelect.addEventListener('change', function() {
        loadClassStudents(this.value);
    });

    // Load initial class if specified in URL
    const urlParams = new URLSearchParams(window.location.search);
    const initialClassId = urlParams.get('class_id');
    if (initialClassId) {
        classSelect.value = initialClassId;
        loadClassStudents(initialClassId);
    }
});

function loadLeaderboard(classId) {
    const tbody = document.getElementById('leaderboard-body');
    
    if (!classId) {
        tbody.innerHTML = '<tr><td colspan="3">Please select a class</td></tr>';
        return;
    }

    tbody.innerHTML = '<tr><td colspan="3" class="loading">Loading leaderboard...</td></tr>';

    fetch(`/api/leaderboard?class_id=${classId}`)
        .then(response => {
            if (!response.ok) throw new Error('Failed to load leaderboard');
            return response.json();
        })
        .then(data => {
            if (data.leaderboard.length === 0) {
                tbody.innerHTML = '<tr><td colspan="3">No students in this class</td></tr>';
                return;
            }

            // Generate leaderboard rows with ranking
            const leaderboardRows = data.leaderboard.map((student, index) => `
                <tr>
                    <td>${index + 1}</td>
                    <td>${student.first_name} ${student.last_name}</td>
                    <td>${student.total_points}</td>
                </tr>
            `).join('');

            tbody.innerHTML = leaderboardRows;
        })
        .catch(error => {
            console.error('Error:', error);
            tbody.innerHTML = '<tr><td colspan="3">Error loading leaderboard</td></tr>';
        });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    const classSelect = document.getElementById('class-select-leaderboard');
    
    // Set default to first available class
    if (classSelect.options.length > 1) { // Skip the "Select a Class" option
        classSelect.value = classSelect.options[1].value;
        loadLeaderboard(classSelect.value);
    }

    classSelect.addEventListener('change', function() {
        loadLeaderboard(this.value);
    });
});