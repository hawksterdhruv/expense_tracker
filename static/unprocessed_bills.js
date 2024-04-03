$(document).ready(function() {
    var getUnprocessedBills = () => {
        var unprocessed_bills_list = $('#unprocessed_bills');
        var unprocessed_bills_item_template = $('#unprocessed_bill_template').html();

        $.ajax({
        type: 'GET',
        url:'api/v1/unprocessed-bills',
        contentType:'application/json',
        success: function(data){
                unprocessed_bills_list.empty();
                $.each(data, function(i,a) {
                    var temp = $(unprocessed_bills_item_template).find('a');
                    temp.html(a.raw_image);
                    temp.attr('href', `/bill/${a.raw_image}`);
                    unprocessed_bills_list.append(temp);
                })
            }
        });
    }
    getUnprocessedBills();

    $('#unprocessed-bill-form').on('submit', function(event) {
        event.preventDefault(); // Prevent the form from submitting via the browser.

        var formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: '/api/v1/unprocessed-bills', // Replace with your upload endpoint
            data: formData,
            processData: false, // Important! Tell jQuery not to process the data
            contentType: false, // Important! Tell jQuery not to set contentType
            success: function(data) {
                console.log('Success:', data);
                $('#successAlert').show().addClass('show');
                getUnprocessedBills();
            },
            error: function(error) {
                console.log('Error:', error);
                // You can add an error notification here
            }
        });
    });
})