$(document).ready(function() {
    $('#addClass').click(function() {
        $('#classModal').modal('show');
        $('#classForm')[0].reset();       
        $('.modal-title').html("<i class='fa fa-plus'></i> Add Class");
        $('#action').val('addClass');
        $('#save').val('Add Class');
    });

    // Ensure that the form is submitted via AJAX to prevent the default form submission behavior
    $('#classForm').submit(function(event) {
        event.preventDefault(); // Prevent the default form submission
        
        // Get form input values
        var className = $('#name').val();

        // Perform validation
        var isValid = true;
        if (className.trim() === '') {
            isValid = false;
            alert('Class name cannot be empty.');
        } else if (className.trim().length > 20) {
            isValid = false;
            alert('Class name cannot exceed 20 characters.');
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
                        alert('Class added successfully!');
                        location.reload(); // Reload the page to update the class list
                    }
                },
                error: function(xhr, status, error) {
                    alert('An error occurred while adding the class: ' + error);
                }
            });
        }
    });
});
