function filterTable() {
    const nameSearch = document.getElementById("name-search").value.toLowerCase();
    const emailSearch = document.getElementById("email-search").value.toLowerCase();
    const table = document.getElementById("user-table");
    const rows = table.getElementsByTagName("tbody")[0].getElementsByTagName("tr");

    for (let i = 1; i < rows.length; i++) {
        const row = rows[i];
        const nameCell = row.getElementsByTagName("td")[0]?.textContent.toLowerCase() || "";
        const emailCell = row.getElementsByTagName("td")[1]?.textContent.toLowerCase() || "";

        const nameMatch = nameCell.includes(nameSearch);
        const emailMatch = emailCell.includes(emailSearch);

        if (nameMatch && emailMatch) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    }
}

function sortTableByRole() {
    const table = document.getElementById("user-table");
    const tbody = table.getElementsByTagName("tbody")[0];
    const rows = Array.from(tbody.getElementsByTagName("tr"));

    const searchRow = rows.shift(); 

    const filter = document.getElementById("role-filter").value;

    rows.sort((a, b) => {
        const roleA = a.getElementsByTagName("td")[2]?.textContent || "";
        const roleB = b.getElementsByTagName("td")[2]?.textContent || "";

        if (filter === "") {
            return 0;
        } else if (roleA === filter && roleB !== filter) {
            return -1;
        } else if (roleA !== filter && roleB === filter) {
            return 1;
        } else {
            return 0;
        }
    });

    tbody.innerHTML = "";
    tbody.appendChild(searchRow); 
    rows.forEach(row => tbody.appendChild(row));
}