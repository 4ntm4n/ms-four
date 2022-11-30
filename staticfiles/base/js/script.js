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
  });
  