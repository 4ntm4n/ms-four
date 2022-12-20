document.addEventListener('DOMContentLoaded', () => {

    //sidenav
    const sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav, {
        edge: "left"
    });

    //authenticated settings user dropdown
    const usrDrop = document.querySelectorAll('.dropdown-trigger');
    M.Dropdown.init(usrDrop, {
        constrainWidth: false,
        coverTrigger: false,
    });


    //collapsible element for requests on profile
    const collapsible = document.querySelectorAll('.collapsible');
    M.Collapsible.init(collapsible)

    //full reference view modal
    const modal = document.querySelectorAll('.modal');
    M.Modal.init(modal);

    const select = document.querySelectorAll('select');
    M.FormSelect.init(select);

    //tooltip for help when hovering element. example at blockquote in send_request_form.html
    const tooltip = document.querySelectorAll('.tooltipped');
    M.Tooltip.init(tooltip, {
        position: "bottom"
    });

    // floating toolbar
    var referenceFab = document.querySelectorAll('.fixed-action-btn');
    M.FloatingActionButton.init(referenceFab, {
        toolbarEnabled: true
    });

    // trigger for pending box in profile
    const pendingBox = document.getElementById('pending-box')
    const pendingTrigger = document.getElementById('pending-trigger')
    const mql = window.matchMedia('(min-width: 600px)');
    const pbGone = pendingBox.style.display === "none"

    let toggle = false

    if (mql.matches && !pbGone) {
        pendingBox.style.display = "none";
    }

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

    mql.onchange = (e) => {
        if (e.matches) {
            pendingBox.style.display = "none";

        } else {
            pendingBox.style.display = "block";
        }
    }
});









const refTbTrigger = document.getElementById("reference-toolbar-trigger");
const refToolbar = document.getElementById("reference-toolbar");
refToolbar.classList.add("scale-out");


refTbTrigger.addEventListener("click", (e) => {
    if (refToolbar.classList.contains("scale-out")) {
        refToolbar.classList.remove("scale-out")
        refToolbar.classList.add("scale-in")
    } else {
        refToolbar.classList.remove("scale-in")
        refToolbar.classList.add("scale-out")
    }

});

