
  document.addEventListener('DOMContentLoaded', function() {
    const datepickerStart = document.querySelectorAll('.datepicker-start');
    M.Datepicker.init(datepickerStart, {
        format: "yyyy-mm-dd",
        firstDay: 1,
        yearRange: 70,
        minDate: new Date("1960-01-01"),
        maxDate: new Date(),
        maxYear: new Date().getFullYear(), 

    });
   
    const selectElement = document.querySelector('.datepicker-start');
    selectElement.addEventListener('change', (event) => {
      minDate = event.target.value;
      const datepickerEnd = document.querySelectorAll('.datepicker-end');
      M.Datepicker.init(datepickerStart, {
          format: "yyyy-mm-dd",
          firstDay: 1,
          yearRange: 70,
          minDate: new Date(minDate),
          maxDate: new Date(),
          maxYear: new Date().getFullYear(), 
      });
    });
  });