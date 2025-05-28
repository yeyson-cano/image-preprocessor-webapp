# Image Preprocessor WebApp

Aplicación web simple para preprocesamiento de imágenes utilizando Flask y OpenCV. Permite aplicar múltiples filtros y transformaciones sobre una o varias imágenes al mismo tiempo, y descargar los resultados en formato `.png` o `.zip`.

## 🚀 Características

- Carga múltiple de imágenes (soporta arrastrar y soltar)
- Aplicación dinámica de múltiples operaciones encadenadas
- Previsualización de parámetros por operación
- Procesamiento y descarga automática de imágenes resultantes
- Interfaz sencilla y responsiva

## 🛠 Tecnologías

- Python 3.x
- Flask
- OpenCV (cv2)
- HTML/CSS/JavaScript

## 📦 Instalación

```bash
# Clona el repositorio
git clone https://github.com/yeyson-cano/image-preprocessor-webapp.git
cd image-preprocessor-webapp

# Crea y activa el entorno virtual
python -m venv venv
source venv/bin/activate   # En Windows usa: venv\Scripts\activate

# Instala las dependencias
pip install -r requirements.txt
