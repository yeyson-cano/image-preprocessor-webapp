import os

class Config:
    # Clave secreta para sesiones (puedes generar una aleatoria segura para producción)
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key"

    # Carpeta donde se guardan temporalmente las imágenes subidas (opcional)
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

    # Extensiones de archivo permitidas
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}

    # Tamaño máximo de archivo (en bytes) — aquí 16 MB por imagen
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # Activar o desactivar el modo debug desde variable de entorno
    DEBUG = os.environ.get("FLASK_DEBUG") == "1"

    # Otras configuraciones específicas podrían ir aquí...
