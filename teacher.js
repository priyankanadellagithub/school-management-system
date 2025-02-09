$(document).ready(function() {
    $('#addTeacher').click(function() {
        $('#teacherModal').modal({
            backdrop: 'static',
            keyboard: false
        });
        
        $("#teacherModal").on("shown.bs.modal", function() {
            $('#teacherForm')[0].reset();
            $('.modal-title').html("<i class='fa fa-plus'></i> Add Teacher");
            $('#action').val('addTeacher');
            $('#save').val('Save');
        });
        $('#closeButton').click(function() {
            $('#teacherModal').modal('hide'); // Manually hide the modal
        });
    });

    // Validate text input
    function validateTextInput(input) {
        return /^[A-Za-z\s]+$/.test(input);
    }

    // Validate phone number
    function validatePhoneNumber(phoneNumber) {
        return /^\d{10}$/.test(phoneNumber);
    }

    // Validate zip code
    function validateZipCode(zipCode) {
        return /^\d+$/.test(zipCode);
    }

    // Ensure that the form is submitted via AJAX to prevent the default form submission behavior
    $('#teacherForm').submit(function(event) {
        event.preventDefault(); // Prevent the default form submission
        
        // Get form input values
        var firstName = $('#first_name').val();
        var lastName = $('#last_name').val();
        var gender = $('#gender').val();
        var phoneNo = $('#phone_no').val();
        var city = $('#city').val();
        var district = $('#district').val();
        var zipCode = $('#zipcode').val();
        
        // Perform validation
        var isValid = true;
        if (!validateTextInput(firstName)) {
            isValid = false;
            alert('Please enter a valid first name (only letters and spaces allowed).');
        }
        if (!validateTextInput(lastName)) {
            isValid = false;
            alert('Please enter a valid last name (only letters and spaces allowed).');
        }
        if (gender.trim() === '') {
            isValid = false;
            alert('Please select a gender.');
        }
        if (!validatePhoneNumber(phoneNo) || phoneNo.trim() === '') {
            isValid = false;
            alert('Please enter a valid phone number (10 digits only).');
        }
        if (!validateTextInput(city)) {
            isValid = false;
            alert('Please enter a valid city name (only letters and spaces allowed).');
        }
        if (!validateTextInput(district)) {
            isValid = false;
            alert('Please enter a valid district name (only letters and spaces allowed).');
        }
        var zipCode = $('#zipcode').val();

        // Validate the zip code
        if (!validateZipCode(zipCode)) {
            alert('Please enter only digits for the zip code.');
            return; // Stop further processing
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
                    // Handle success response from the server
                    if (response.startsWith("Error:")) {
                        alert(response); // Display the error message
                    } else {
                        alert('Teacher added successfully!');
                        location.reload(); // Reload the page to update the teacher list
                    }
                },
                error: function(xhr, status, error) {
                    // Handle error response from the server
                    alert('An error occurred while adding the teacher: ' + error);
                }
            });
        }
    });
});
