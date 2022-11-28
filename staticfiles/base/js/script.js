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


  });
  