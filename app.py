# app.py

import os
import io
import zipfile

import cv2
import numpy as np

from flask import (
    Flask,
    render_template,
    request,
    send_file,
    abort
)
from werkzeug.utils import secure_filename

from config import Config
from utils import allowed_file
from image_ops import apply_operations  # <-- importamos la función en lote

# --------------------------------------------------
# Inicialización de la app
# --------------------------------------------------
app = Flask(__name__)
app.config.from_object(Config)


# --------------------------------------------------
# Ruta GET / → formulario
# --------------------------------------------------
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# --------------------------------------------------
# Ruta POST /process → procesar y devolver imágenes
# --------------------------------------------------
@app.route('/process', methods=['POST'])
def process():
    # 1) Recogemos la(s) imagen(es) subidas
    uploaded_files = request.files.getlist('images')
    if not uploaded_files:
        abort(400, "No se subió ninguna imagen.")

    # 2) Recogemos la lista de operaciones en orden
    operations = request.form.getlist('operations[]')
    if not operations:
        abort(400, "Debe seleccionar al menos una operación.")

    # 3) Todos los parámetros en un dict
    params = request.form.to_dict(flat=True)

    processed = []  # lista de tuplas (filename, bytes_data)

    for f in uploaded_files:
        filename = secure_filename(f.filename)
        if not filename or not allowed_file(filename):
            continue  # saltamos nombres inválidos

        # 4) Leemos y decodificamos la imagen
        file_bytes = f.read()
        img_array = np.frombuffer(file_bytes, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        if img is None:
            continue  # no se pudo decodificar

        # 5) Aplicamos TODAS las operaciones en secuencia
        result = apply_operations(img, operations, params)

        # 6) Re-encode a PNG
        success, buf = cv2.imencode('.png', result)
        if not success:
            continue

        out_bytes = buf.tobytes()
        base, _ = os.path.splitext(filename)
        out_name = f"processed_{base}.png"
        processed.append((out_name, out_bytes))

    if not processed:
        abort(400, "No se procesó ninguna imagen válida.")

    # 7) Devolvemos el/los resultados
    if len(processed) == 1:
        name, data = processed[0]
        return send_file(
            io.BytesIO(data),
            mimetype='image/png',
            as_attachment=True,
            download_name=name
        )

    # Varias imágenes → ZIP
    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for name, data in processed:
            z.writestr(name, data)
    zip_buf.seek(0)

    return send_file(
        zip_buf,
        mimetype='application/zip',
        as_attachment=True,
        download_name='processed_images.zip'
    )


# --------------------------------------------------
# Manejo de errores HTTP
# --------------------------------------------------
@app.errorhandler(400)
def bad_request(e):
    return f"<h1>400 Bad Request</h1><p>{e.description}</p>", 400


# --------------------------------------------------
# Lanzamiento
# --------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
