document.addEventListener('DOMContentLoaded', function () {

    // find the toolbox button
    const refTbTrigger = document.getElementById("reference-toolbar-trigger");
    const refToolbar = document.getElementById("reference-toolbar");
    //add scaleout class to hide on default
    refToolbar.classList.add("scale-out");

    //toggle toolbox function
    refTbTrigger.addEventListener("click", (e) => {
        if (refToolbar.classList.contains("scale-out")) {
            refToolbar.classList.remove("scale-out")
            refToolbar.classList.add("scale-in")
        } else {
            refToolbar.classList.remove("scale-in")
            refToolbar.classList.add("scale-out")
        }

    });

});