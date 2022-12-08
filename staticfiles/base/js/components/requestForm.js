document.addEventListener('DOMContentLoaded', function() {
    // find date from and date to input fields
    const dateFromInput = document.getElementById('id_date_from');
    const dateToInput = document.getElementById('id_date_to');

    //if jS loaded, set date to disabled as default state.
    dateToInput.setAttribute("disabled", true);
    
    const datepickerStart = document.getElementById('id_date_from');
    M.Datepicker.init(datepickerStart, {
        format: "yyyy-mm-dd",
        firstDay: 1,
        yearRange: 70,
        minDate: new Date("1960-01-01"),
        maxDate: new Date(),
        maxYear: new Date().getFullYear(), 


    });

    dateFromInput.addEventListener('change', (event) => {
        const selectedDate = event.target.value;
        date1 = new Date(selectedDate);
        
        

        const datepickerEnd = document.getElementById('id_date_to');
        M.Datepicker.init(datepickerEnd, {
            format: 'yyyy-mm-dd',
            firstDay: 1,
            yearRange: 20,
            minDate: new Date(selectedDate),
            maxDate: new Date(),
            maxYear: new Date().getFullYear(), 
        });
        
        dateToInput.disabled=false;
    });

   // if from date is NaN, tell user to fill in that date first.
    dateToInput.addEventListener('click', (event) => {
        if (dateFromInput.value === ""){
            alert("enter from date first")
        };       
    })
   
});