// Versión mejorada con verificación
document.addEventListener('DOMContentLoaded', function() {
  const btnMenu = document.getElementById('btn-menu');
  const menu = document.getElementById('menu');
  
  if (btnMenu && menu) {
    btnMenu.addEventListener('click', function() {
      this.classList.toggle('activo');
      menu.classList.toggle('mostrar');
    });
  } else {
    console.error('No se encontraron los elementos del menú');
  }
});