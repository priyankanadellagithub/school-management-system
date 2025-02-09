$(document).ready(function() {
    $('#addMarks').click(function() {
        $('#marksModal').modal('show');
        $('#marksForm')[0].reset();
        $('.modal-title').html("<i class='fa fa-plus'></i> Add Marks");
        $('#action').val('addMarks');
        $('#save').val('Save');
    });

    $('#marksForm').submit(function(event) {
        event.preventDefault();
        
        // Get form input values
        var studentId = $('#student_id').val();
        var courseId = $('#course_id').val();
        var marksScored = $('#marks_scored').val();
        
        // Perform validation
        var isValid = true;
        if (isNaN(studentId) || studentId.trim() === '') {
            isValid = false;
            alert('Please enter a valid student ID.');
        }
        if (isNaN(courseId) || courseId.trim() === '') {
            isValid = false;
            alert('Please enter a valid course ID.');
        }
        if (isNaN(marksScored) || marksScored.trim() === '' || marksScored < 0 || marksScored > 100) {
            isValid = false;
            alert('Please enter a valid marks score between 0 and 100.');
        }
        
        // If all fields are valid, submit the form
        if (isValid) {
            var formData = $(this).serialize();
            $.ajax({
                type: 'POST',
                url: $(this).attr('action'),
                data: formData,
                success: function(response) {
                    if (response.startsWith("Error:")) {
                        alert(response); // Display the error message
                    } else {
                        alert('Marks added successfully!');
                        location.reload();
                    }
                },
                error: function(xhr, status, error) {
                    alert('An error occurred while adding the marks: ' + error);
                }
            });
        }
    });
});
