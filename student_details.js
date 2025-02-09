function fetchStudentsInClass(classId) {
    if (classId) {
        fetch(`/get_students_in_class/${classId}`)
            .then(response => response.json())
            .then(data => {
                const studentsList = document.getElementById('students_list');
                const studentsCount = document.getElementById('students_count');
                studentsList.innerHTML = ''; // Clear previous data
                studentsCount.innerHTML = ''; // Clear previous data

                // Create the table element
                const table = document.createElement('table');
                table.className = 'table table-striped';

                // Create table headers
                const thead = document.createElement('thead');
                const headerRow = document.createElement('tr');
                ['Student ID', 'First Name', 'Last Name'].forEach(text => {
                    const th = document.createElement('th');
                    th.textContent = text;
                    headerRow.appendChild(th);
                });
                thead.appendChild(headerRow);
                table.appendChild(thead);

                // Create table body
                const tbody = document.createElement('tbody');
                data.forEach(student => {
                    const row = document.createElement('tr');
                    ['student_id', 'first_name', 'last_name'].forEach(field => {
                        const cell = document.createElement('td');
                        cell.textContent = student[field];
                        row.appendChild(cell);
                    });
                    tbody.appendChild(row);
                });
                table.appendChild(tbody);

                studentsList.appendChild(table);

                // Display number of students
                const countHTML = `<p>Number of students in class: ${data.length}</p>`;
                studentsCount.innerHTML = countHTML;
            })
            .catch(error => console.error('Error:', error));
    }
}
