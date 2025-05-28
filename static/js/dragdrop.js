// static/js/dragdrop.js

document.addEventListener('DOMContentLoaded', () => {
  const dropArea = document.getElementById('drop-area');
  const fileInput = document.getElementById('images');
  const dropZone = document.getElementById('drop-zone');
  const fileNames = document.getElementById('file-names');

  // Evitar comportamiento por defecto para estos eventos
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, e => {
      e.preventDefault();
      e.stopPropagation();
    });
  });

  // Estilos al arrastrar sobre la zona
  ['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => {
      dropArea.classList.add('highlight');
    });
  });
  ['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => {
      dropArea.classList.remove('highlight');
    });
  });

  // Al soltar archivos
  dropArea.addEventListener('drop', e => {
    const dt = e.dataTransfer;
    const files = dt.files;
    fileInput.files = files; // asigna al input
    updateFileList(files);
  });

  // Al hacer clic en la zona, abre el diálogo de archivos
  dropZone.addEventListener('click', () => fileInput.click());

  // Al seleccionar por el diálogo de archivos
  fileInput.addEventListener('change', () => {
    updateFileList(fileInput.files);
  });

  // Muestra los nombres de los archivos seleccionados
  function updateFileList(files) {
    fileNames.innerHTML = '';
    Array.from(files).forEach(file => {
      const p = document.createElement('p');
      p.textContent = file.name;
      fileNames.appendChild(p);
    });
  }
});
