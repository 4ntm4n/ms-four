document.addEventListener('DOMContentLoaded', function () {
    // find pending-box and trigger switch
    const pendingBox = document.getElementById('pending-box')
    const pendingTrigger = document.getElementById('pending-trigger')
    
    //catching screen widths of 600px or larger and save as mql.
    const mql = window.matchMedia('(min-width: 600px)');
    // on larger screens pending box should be gone.
    const pbGone = pendingBox.style.display === "none"

    //set toggle switch to off by default to match switch styling
    let toggle = false

    if (mql.matches && !pbGone) {
        pendingBox.style.display = "none";
    }

    // toggle switch function for pending box
    pendingTrigger.onclick = (e) => {
        const pbGone = pendingBox.style.display === "none";
        if (pbGone && !toggle) {
            toggle = true;
            pendingBox.style.display = "block";
        } else {
            toggle = false;
            pendingBox.style.display = "none";
        }
    }

    /*   
        * look for changes that matches screen width 'mql' 
        * and make pending box visible on small screens. 
    */
    mql.onchange = (e) => {
        if (e.matches) {
            pendingBox.style.display = "none";

        } else {
            pendingBox.style.display = "block";
        }
    }
});