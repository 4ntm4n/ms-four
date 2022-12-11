document.addEventListener('DOMContentLoaded', () => {
    
    //sidenav
    const sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav, {
        edge: "left",
        draggable: false,
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
  });
  



