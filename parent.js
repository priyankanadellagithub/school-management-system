$(document).ready(function() {
    $('#addParent').click(function() {
        $('#parentModal').modal({
            backdrop: 'static',
            keyboard: false
        });
        
        $("#parentModal").on("shown.bs.modal", function() {
            $('#parentForm')[0].reset();
            $('.modal-title').html("<i class='fa fa-plus'></i> Add Parent");
            $('#action').val('addParent');
            $('#save').val('Save');
        });
        $('#closeButton').click(function() {
            $('#parentModal').modal('hide'); // Manually hide the modal
        });
    });

    // Ensure that the form is submitted via AJAX to prevent the default form submission behavior
    $('#parentForm').submit(function(event) {
        event.preventDefault(); // Prevent the default form submission
        
        // Get form input values
        var firstName = $('#first_name').val();
        var lastName = $('#last_name').val();
        var studentId = $('#student_id').val();
        var phoneNumber = $('#phone_no').val();
        var relationship = $('#relationship_with_student').val();
        var email = $('#email').val();

        // Perform validation
        var isValid = true;
        if (!isTextOnly(firstName)) {
            isValid = false;
            alert('First name should contain text only.');
        }
        if (!isTextOnly(lastName)) {
            isValid = false;
            alert('Last name should contain text only.');
        }
        if (studentId.trim() === '' || isNaN(studentId)) {
            isValid = false;
            alert('Please enter a valid student ID.');
        }
        if (phoneNumber.trim() !== '' && !validatePhoneNumber(phoneNumber)) {
            isValid = false;
            alert('Please enter a valid phone number (10 digits only) for Phone No.');
        }
        if (!isTextOnly(relationship)) {
            isValid = false;
            alert('Relationship with student should contain text only.');
        }
        if (email.trim() !== '' && !validateEmail(email)) {
            isValid = false;
            alert('Please enter a valid email address for Email.');
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
                        alert(response); // Display the general error message
                    } else if (response.startsWith("Duplicate entry")) {
                        alert('Duplicate parent details. Please enter unique parent details.'); // Display the custom error message for duplicate entry
                    } else {
                        alert('Parent added successfully!');
                        location.reload(); // Reload the page to update the parent list
                    }
                },
                error: function(xhr, status, error) {
                    // Handle error response from the server
                    alert('An error occurred while adding the parent: ' + error);
                }
            });
        }
    });

    // Validate email format
    function validateEmail(email) {
        var re = /\S+@\S+\.\S+/;
        return re.test(email);
    }

    // Validate phone number format
    function validatePhoneNumber(phoneNumber) {
        var re = /^\d{10}$/; // Assuming phone number is 10 digits
        return re.test(phoneNumber);
    }

    // Custom validation function to check if input contains only text
    function isTextOnly(input) {
        var re = /^[A-Za-z]+$/;
        return re.test(input);
    }
});
