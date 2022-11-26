document.addEventListener('DOMContentLoaded', function() {
    
    options = {
        edge: "left",
        draggable: false,
    }

    const elem = document.querySelectorAll('.sidenav');
    const instance = M.Sidenav.init(elem, options);
  });
  