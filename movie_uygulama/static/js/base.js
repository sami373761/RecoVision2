$(document).ready(function() {
    $('.navbar-toggler').on('click', function() {
      $('#navbarTogglerDemo01').collapse('toggle');
    });
  });


document.addEventListener("DOMContentLoaded", function() {
  const defaultNav = document.getElementById("defaultNav");
  const altNav = document.getElementById("altNav");

  function checkNavbarSize() {
      if (window.innerWidth <= 992) {
          defaultNav.classList.add("d-none"); 
          altNav.classList.remove("d-none"); 
      } else {
          defaultNav.classList.remove("d-none"); 
          altNav.classList.add("d-none");  
      }
  }

  checkNavbarSize();
  window.addEventListener("resize", checkNavbarSize);
});




function toggleProfileVisibility() {
  const profileElement = document.getElementById('profile');
  
  if (window.innerWidth <= 992) {
    profileElement.style.display = 'none';
  } else {
    profileElement.style.display = 'block';
  }
}
toggleProfileVisibility();
window.addEventListener('resize', toggleProfileVisibility);


