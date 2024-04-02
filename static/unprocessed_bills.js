$(document).ready(function() {
    var unprocessed_bills_list = $('#unprocessed_bills');
    var unprocessed_bills_item_template = $('#unprocessed_bill_template').html();

    $.ajax({
    type: 'GET',
    url:'api/v1/unprocessed-bills',
    contentType:'application/json',
    success: function(data){
            $.each(data, function(i,a) {
                var temp = $(unprocessed_bills_item_template).find('a')
                temp.html(a.raw_image);
                temp.attr('href', a.raw_image);
                unprocessed_bills_list.append(temp);
            })
        }
    })
})