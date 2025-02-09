// student_marks_report.js

let chart; // Declare chart variable outside the function

function fetchStudentMarks(studentId) {
    if (studentId) {
        fetch(`/get_student_marks/${studentId}`)
            .then(response => response.json())
            .then(data => {
                const marksReport = document.getElementById('marks_report');
                marksReport.innerHTML = ''; // Clear previous data

                // Create the table
                const table = document.createElement('table');
                table.className = 'table table-striped';
                const thead = document.createElement('thead');
                const tbody = document.createElement('tbody');

                const headerRow = document.createElement('tr');
                ['First Name', 'Last Name', 'Course', 'Marks Scored'].forEach(text => {
                    const th = document.createElement('th');
                    th.textContent = text;
                    headerRow.appendChild(th);
                });
                thead.appendChild(headerRow);

                // Populate the table
                data.forEach(row => {
                    const tr = document.createElement('tr');
                    ['first_name', 'last_name', 'course', 'marks_scored'].forEach(field => {
                        const td = document.createElement('td');
                        td.textContent = row[field];
                        tr.appendChild(td);
                    });
                    tbody.appendChild(tr);
                });

                table.appendChild(thead);
                table.appendChild(tbody);
                marksReport.appendChild(table);

                // Destroy existing chart instance if it exists
                if (chart) {
                    chart.destroy();
                }

                // Create the chart
                const ctx = document.getElementById('marks_chart').getContext('2d');
                chart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: data.map(row => row.course),
                        datasets: [{
                            label: 'Marks Scored',
                            data: data.map(row => row.marks_scored),
                            backgroundColor: 'rgba(54, 162, 235, 0.5)',
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 100 // Set maximum value for y-axis
                            }
                        },
                        // Reduce the width of the bars
                        barThickness: 20 // Adjust the value as needed
                    }
                });
            })
            .catch(error => console.error('Error:', error));
    }
}
