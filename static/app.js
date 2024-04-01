$(document).ready(function() {
    $('#bill-form').on('submit', function(event) {
        event.preventDefault(); // Prevent the form from submitting via the browser.

        var formData = {
            date_of_expense: $('#dateOfExpense').val(),
            tax_amount: $('#taxAmount').val(),
//            items: $('#items').val().split('\n'), // Split the textarea content into an array of items.
            image: $('#image').val(),
            raw_image: $('#rawImage').val()
        };
        $.ajax({
            type: 'POST',
            url: 'api/v1/bills',
            data: JSON.stringify(formData),
            contentType: 'application/json',
            success: function(data) {
                console.log('Success:', data);
                $('#successAlert').show().addClass('show');
            },
            error: function(error) {
                console.log('Error:', error);
            }
        });
    });
});