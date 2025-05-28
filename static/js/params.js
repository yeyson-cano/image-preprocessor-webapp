// static/js/params.js

document.addEventListener('DOMContentLoaded', () => {
  const template = document.getElementById('operation-template');
  const container = document.getElementById('operations-container');
  const addBtn = document.getElementById('add-operation');

  // Definición de campos de parámetros para cada operación
  const paramFields = {
    rescale: `
      <label>Factor X: <input type="number" name="fx" step="0.1" value="1.0" required></label>
      <label>Factor Y: <input type="number" name="fy" step="0.1" value="1.0" required></label>
    `,
    histogram: `<p>(No requiere parámetros)</p>`,
    equalize: `<p>(No requiere parámetros)</p>`,
    linear_filter: `
      <label>Tamaño del kernel: 
        <input type="number" name="kernel_size" value="5" min="1" step="2" required>
      </label>
    `,
    nonlinear_filter: `
      <label>Tamaño del kernel: 
        <input type="number" name="ksize" value="5" min="1" step="2" required>
      </label>
    `,
    translate: `
      <label>Traslación X (px): <input type="number" name="tx" value="0" step="1" required></label>
      <label>Traslación Y (px): <input type="number" name="ty" value="0" step="1" required></label>
    `,
    rotate: `
      <label>Ángulo (grados): <input type="number" name="angle" value="0" step="1" required></label>
      <label>Escala: <input type="number" name="scale" value="1.0" step="0.1" required></label>
    `
  };

  // Crea un bloque de operación a partir de la plantilla
  function createOperationBlock() {
    const clone = template.content.cloneNode(true);
    const block = clone.querySelector('.operation-block');
    const select = block.querySelector('.operation-select');
    const paramsDiv = block.querySelector('.operation-params');
    const removeBtn = block.querySelector('.remove-operation');

    // Cuando cambie la operación, actualiza los parámetros
    select.addEventListener('change', () => {
      const op = select.value;
      paramsDiv.innerHTML = paramFields[op] || '';
    });

    // Botón para quitar este bloque
    removeBtn.addEventListener('click', () => {
      block.remove();
    });

    return block;
  }

  // Al hacer clic en "+ Añadir Operación", agregamos un nuevo bloque
  addBtn.addEventListener('click', () => {
    const block = createOperationBlock();
    container.appendChild(block);
  });

  // Opcional: crea un bloque al cargar la página
  addBtn.click();
});
