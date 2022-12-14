document.addEventListener('DOMContentLoaded', () => {
    
    //sidenav
    const sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav, {
        edge: "left"
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

    const pendingBox = document.getElementById('pending-box')
    const pendingTrigger = document.getElementById('pending-trigger')
    const mql = window.matchMedia('(min-width: 600px)');
    const pbGone = pendingBox.classList.contains('scale-out')

    let toggle = false

    alert(mql.matches)
    if (mql.matches && !pbGone){
        pendingBox.classList.add("scale-out")
    }

    pendingTrigger.onclick = (e) => {
        const pbGone = pendingBox.classList.contains('scale-out')
        if (pbGone && !toggle){
            toggle = true;
            pendingBox.classList.add('scale-in')
        }else{
            toggle = false;
            pendingBox.classList.remove('scale-in')
        }
    }

    mql.onchange = (e) =>{
        e.matches ? pendingBox.classList.add('scale-out')
                  : pendingBox.classList.remove('scale-out');
    }


});









const refTbTrigger = document.getElementById("reference-toolbar-trigger");
const refToolbar = document.getElementById("reference-toolbar");
refToolbar.classList.add("scale-out");


refTbTrigger.addEventListener("click", (e) => {
    if (refToolbar.classList.contains("scale-out")){
        refToolbar.classList.remove("scale-out")
        refToolbar.classList.add("scale-in")
    }else {
        refToolbar.classList.remove("scale-in")
        refToolbar.classList.add("scale-out")
    }
        
});

