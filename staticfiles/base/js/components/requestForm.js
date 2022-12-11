document.addEventListener('DOMContentLoaded', function() {
    //find  id_company_name and from-to-helper field
    const companyField = document.getElementById('id_company_name');
    let fromToHelper = document.getElementById('from-to-helper');
    
    companyField.addEventListener('change', (event) => {
        const company = event.target.value;
        fromToHelper.innerHTML = `between what dates did you work at ${company}?`
    });

    //find to date imput field
    const toDate = document.getElementById("id_date_to");

    // "from_date" datepicker with initial settings.
    const datepickerStart = document.getElementById('id_date_from');
    let startDate = M.Datepicker.init(datepickerStart, {
        format: 'yyyy-mm-dd',
        firstDay: 1,
        yearRange: 70,
        minDate: new Date("1960-01-01"),
        maxDate: new Date(),
        maxYear: new Date().getFullYear(), 
        onSelect: function(date){
            //set min date to
            endDate.options.minDate = new Date(date);
            endDate.gotoDate(date);
            if (date > endDate.date){
                endDate.setDate(date);
                //set value of toDate input field to the same date if date > toDate
                toDate.value = `${
                    date.getFullYear()}-${
                        date.getMonth() +1}-${
                            String(date.getDate()).padStart(2, '0')
                        }`;
            }
        }
    });

    // "to_date" date picker with initial settings.
    const datepickerEnd = document.getElementById('id_date_to');
    let endDate = M.Datepicker.init(datepickerEnd, {
        format: 'yyyy-mm-dd',
        firstDay: 1,
        yearRange: 20,
        maxDate: new Date(),
        maxYear: new Date().getFullYear(),
    });
   


    const emailField = document.getElementById("id_to_email");


    emailField.addEventListener("change", (e) => {
        const extensionNotice = document.getElementById("extension-notice");
        const badExtensions = ["gmail.com", "outlook.com", "live.com", "hotmail.com", "yahoo.com"]

        const toEmailExt = e.target.value.split("@").pop();
        
        let match = false;
        for (let extension of badExtensions){                             
            if (toEmailExt === extension) {
                match = true; 
            } 
        }
        match ? extensionNotice.style.visibility = "visible" : extensionNotice.style.visibility = "hidden"
    });
});