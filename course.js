$(document).ready(function() {
    $('#addCourse').click(function() {
        $('#courseModal').modal('show');
        $('#courseForm')[0].reset();
        $('.modal-title').html("<i class='fa fa-plus'></i> Add Course");
        $('#action').val('addCourse');
        $('#save').val('Save');
    });

    // Ensure that the form is submitted via AJAX to prevent the default form submission behavior
    $('#courseForm').submit(function(event) {
        event.preventDefault();
        
        // Get form input values
        var courseId = $('#course_id').val();
        var courseName = $('#name').val();
        var teacherId = $('#teacher_id').val();
        var classId = $('#class_id').val();

        // Perform validation
        var isValid = true;
        if (courseId.trim() === '' || isNaN(courseId)) {
            isValid = false;
            alert('Please enter a valid course ID.');
        }
        if (courseName.trim() === '') {
            isValid = false;
            alert('Course name cannot be empty.');
        } else if (!/^[a-zA-Z\s]+$/.test(courseName)) {
            isValid = false;
            alert('Course name must contain only letters and spaces.');
        }
        if (teacherId.trim() === '' || isNaN(teacherId)) {
            isValid = false;
            alert('Please enter a valid teacher ID.');
        }
        if (classId.trim() === '' || isNaN(classId)) {
            isValid = false;
            alert('Please enter a valid class ID.');
        }

        // If all fields are valid, submit the form
        if (isValid) {
            // Serialize form data
            var formData = $(this).serialize();
            
            // Make an AJAX POST request to the server to submit the form data
            $.ajax({
                type: 'POST',
                url: $(this).attr('action'),
                data: formData,
                success: function(response) {
                    // Check if the response contains an error message
                    if (response.startsWith("Error:")) {
                        alert(response); // Display the error message
                    } else {
                        alert('Course added successfully!');
                        location.reload(); // Reload the page to update the course list
                    }
                },
                error: function(xhr, status, error) {
                    alert('An error occurred while adding the course: ' + error);
                }
            });
        }
    });
});


