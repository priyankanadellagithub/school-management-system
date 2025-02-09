$(document).ready(function() {
    $('#addStudent').click(function() {
        $('#studentModal').modal({
            backdrop: 'static',
            keyboard: false
        });
        
        $("#studentModal").on("shown.bs.modal", function() {
            $('#studentForm')[0].reset();
            $('.modal-title').html("<i class='fa fa-plus'></i> Add Student");
            $('#action').val('addStudent');
            $('#save').val('Save');
        });
        $('#closeButton').click(function() {
            $('#studentModal').modal('hide'); // Manually hide the modal
        });
    });

    // Validate date of birth format
    function validateDateOfBirth(date) {
        var re = /^\d{4}-\d{2}-\d{2}$/; // Assuming date format is YYYY-MM-DD
        return re.test(date);
    }

    function validateTextInput(input) {
        return /^[A-Za-z\s]+$/.test(input);
    }

    function validateZipCode(zip_Code) {
        return /^\d+$/.test(zip_Code);
    }

    // Ensure that the form is submitted via AJAX to prevent the default form submission behavior
    $('#studentForm').submit(function(event) {
        event.preventDefault(); // Prevent the default form submission
        
        // Get form input values
        var studentId = $('#student_id').val();
        var schoolId = $('#school_id').val();
        var firstName = $('#first_name').val();
        var lastName = $('#last_name').val();
        var dob = $('#dob').val();
        var academicYear = $('#academic_year').val();
        var city = $('#city').val();
        var zipCode = $('#zip_code').val();
        var caste = $('#caste').val();

        // Perform validation
        var isValid = true;
        if (isNaN(studentId) || studentId.trim() === '') {
            isValid = false;
            alert('Please enter a valid student ID.');
        }
        if (isNaN(schoolId) || schoolId.trim() === '') {
            isValid = false;
            alert('Please enter a valid school ID.');
        }
        if (!validateTextInput(firstName)) {
            isValid = false;
            alert('Please enter a valid first name (only letters and spaces allowed).');
        }
        if (!validateTextInput(lastName)) {
            isValid = false;
            alert('Please enter a valid last name (only letters and spaces allowed).');
        }
        if (!validateDateOfBirth(dob)) {
            isValid = false;
            alert('Please enter a valid date of birth (YYYY-MM-DD).');
        }
        if (isNaN(academicYear) || academicYear.trim() === '') {
            isValid = false;
            alert('Please enter a valid academic year.');
        }
        if (!validateTextInput(city)) {
            isValid = false;
            alert('Please enter a valid city name (only letters and spaces allowed).');
        }
        // Validate the zip code
        if (!validateZipCode(zipCode)) {
            alert('Please enter only digits for the zip code.');
            return; // Stop further processing
        }
        if (!validateTextInput(caste)) {
            isValid = false;
            alert('Please enter a valid caste name (only letters and spaces allowed).');
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
                        alert('Student added successfully!');
                        location.reload(); // Reload the page to update the student list
                    }
                },
                error: function(xhr, status, error) {
                    alert('An error occurred while adding the student: ' + error);
                }
            });
        }
    });
});



