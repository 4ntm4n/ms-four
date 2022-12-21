document.addEventListener('DOMContentLoaded', function() {
    const othRelation = document.getElementById("id_other_relation");
    //hide inputfield and label by defauld
    othRelation.style.visibility = "hidden";
    othRelation.nextElementSibling.style.visibility = "hidden"   
    
    // function that toggle visibilty and requirement of other choice.
    const toggleVisibility = (choice) => {   
        if (choice === "Other"){
            othRelation.style.visibility = "visible";
            othRelation.setAttribute("required", true)
            othRelation.nextElementSibling.style.visibility = "visible"
        }else{
            othRelation.style.visibility = "hidden";
            othRelation.nextElementSibling.style.visibility = "hidden"
            othRelation.removeAttribute("required")

        }
    };

    //get the relation selection Input field.
    const selectionInput = document.querySelector(".select-dropdown.dropdown-trigger")
    
    // listen for change on the relation selection input.
    selectionInput.onselectionchange = (e) =>{
        const select = e.target.value;
        toggleVisibility(select)
    }

});