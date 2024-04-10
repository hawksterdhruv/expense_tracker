$(document).ready(function () {
  var rawData = $("#raw-data");
  $("#process").click(function () {
    $.ajax({
      type: "GET",
      url: `/api/v1/process/${$(this).data("target")}`,
      contentType: "application/json",
      success: function (data) {
        rawData.empty();
        $.each(data["data"], function (i, a) {
          if (a !== "") {
            rawData.append(`<tr><td>${a}</td><tr>`);
          }
        });
      },
    });
  });
  var thisAmazingFunction = ()=>{
    console.log(e.target)
  }

  var fields = ['date', 'total', 'tax', 'items'];
  var bill = {}
  var inputField = $('#randomId')
  // Check global has #process been clicked
  // logic for early exit ? detect Escape? detect right click ? 
  // 
  $("#add-bill").click(function () {
    fields.forEach(element => {
        if (element in bill){
          
          inputField.attr('placeholder',`Enter ${element}`);
          inputField.show();
          rawData.addEventListener('click', thisAmazingFunction, true);
            // show input box.
            // allow clicking ? 

        }

    });
  });
});
