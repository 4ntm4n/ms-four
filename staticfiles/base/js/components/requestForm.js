document.addEventListener('DOMContentLoaded', function() {
    const datepickerStart = document.getElementById('id_date_from');
    M.Datepicker.init(datepickerStart, {
        format: "yyyy-mm-dd",
        firstDay: 1,
        yearRange: 70,
        minDate: new Date("1960-01-01"),
        maxDate: new Date(),
        maxYear: new Date().getFullYear(), 

    });

    const dateInput = document.getElementById('id_date_from');
    dateInput.addEventListener('change', (event) => {
    selectedDate = event.target.value;

        const datepickerEnd = document.getElementById('id_date_to');
        M.Datepicker.init(datepickerEnd, {
            format: "yyyy-mm-dd",
            firstDay: 1,
            yearRange: 70,
            minDate: new Date(selectedDate),
            maxDate: new Date(),
            maxYear: new Date().getFullYear(), 
        });
      
    });

});