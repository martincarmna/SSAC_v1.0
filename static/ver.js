document.addEventListener('DOMContentLoaded', () => {
  const btnFiltro = document.getElementById('btnFiltro');
  const filtroDropdown = document.getElementById('filtroDropdown');

  btnFiltro.addEventListener('click', () => {
    if (filtroDropdown.style.display === 'none' || filtroDropdown.style.display === '') {
      filtroDropdown.style.display = 'block';
    } else {
      filtroDropdown.style.display = 'none';
    }
  });
});
