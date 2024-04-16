$(document).ready(function () {
  let rawData = $("#raw-data");
  let table = rawData.children('table');
  let billImage = rawData.children('img')
  $("#process").click(function () {
    $.ajax({
      type: "GET",
      url: `/api/v1/process/${$(this).data("target")}`,
      contentType: "application/json",
      success: function (data) {
        table.empty();
        billImage.addClass('d-none')
        billImage.removeClass('d-none').addClass('d-block')
        $.each(data["data"], function (i, a) {
          if (a !== "") {
            table.append(`<tr><td>${a}</td><tr>`);
          }
        });
      },
    });
  });

  let form = $("#bill-form");
  let steps = $(".step");
  let prevBtn = $("#prev-btn");
  let nextBtn = $("#next-btn");
  let submitBtn = $("#submit-btn");
  form.onsubmit = () => {
    return false;
  };
  let currentStep = 0;
  let stepCount = steps.length;
  steps.removeClass("d-block").addClass("d-none");
  $(steps[currentStep]).addClass("d-block");
  if (currentStep == 0) {
    prevBtn.addClass("d-none");
    submitBtn.addClass("d-none");
    nextBtn.addClass("d-inline-block");
  }

  nextBtn.click(() => {
    let previousStep = currentStep;
    currentStep++;
    if (currentStep > 0 && currentStep < stepCount - 1) {
      showMiddleStep(currentStep, previousStep);
    } else if (currentStep == stepCount - 1) {
      showLastStep(currentStep, previousStep);
    }
  });

  prevBtn.click(() => {
    let previousStep = currentStep;
    currentStep--;
    if (currentStep > 0 && currentStep < stepCount - 1) {
      showMiddleStep(currentStep, previousStep);
    } else if (currentStep == 0) {
      showMiddleStep(currentStep, previousStep);
      prevBtn.removeClass("d-inline-block").addClass("d-none");
    }
  });
  function showMiddleStep(currentStep, previousStep) {
    console.log('showing middle step for step: ', currentStep, ' with prevStep: ', previousStep)
    prevBtn.removeClass("d-none").addClass("d-inline-block");
    nextBtn.removeClass("d-none").addClass("d-inline-block");
    submitBtn.removeClass("d-inline-block").addClass("d-none");

    $(steps[currentStep]).addClass("d-block").removeClass("d-none");
    $(steps[previousStep]).addClass("d-none").removeClass("d-block");
  }
  function showLastStep(currentStep, previousStep) {
    console.log('showing last step for step: ', currentStep, ' with prevStep: ', previousStep)

    $(steps[currentStep]).removeClass("d-none").addClass("d-block");
    $(steps[previousStep]).addClass("d-none").removeClass("d-block");
    prevBtn.removeClass("d-none").addClass("d-inline-block");
    nextBtn.removeClass("d-inline-block").addClass("d-none");
    submitBtn.removeClass("d-none").addClass("d-inline-block");
  }
});
