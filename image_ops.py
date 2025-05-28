# image_ops.py

import cv2
import numpy as np

def rescale(img: np.ndarray, fx: float = 1.0, fy: float = 1.0,
            interpolation: int = cv2.INTER_LINEAR) -> np.ndarray:
    return cv2.resize(img, None, fx=fx, fy=fy, interpolation=interpolation)


def histogram(img: np.ndarray, draw: bool = False) -> np.ndarray:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])

    if not draw:
        return hist

    hist_img = np.zeros((300, 256), dtype=np.uint8)
    cv2.normalize(hist, hist, 0, hist_img.shape[0], cv2.NORM_MINMAX)
    for x, y in enumerate(hist.flatten()):
        cv2.line(hist_img, (x, hist_img.shape[0]),
                 (x, hist_img.shape[0] - int(y)), 255)
    return cv2.cvtColor(hist_img, cv2.COLOR_GRAY2BGR)


def equalize(img: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eq = cv2.equalizeHist(gray)
    return cv2.cvtColor(eq, cv2.COLOR_GRAY2BGR)


def linear_filter(img: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    k = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size**2)
    return cv2.filter2D(img, -1, k)


def nonlinear_filter(img: np.ndarray, ksize: int = 5) -> np.ndarray:
    return cv2.medianBlur(img, ksize)


def translate(img: np.ndarray, tx: float = 0, ty: float = 0) -> np.ndarray:
    rows, cols = img.shape[:2]
    M = np.array([[1, 0, tx],
                  [0, 1, ty]], dtype=np.float32)
    return cv2.warpAffine(img, M, (cols, rows))


def rotate(img: np.ndarray, angle: float = 0, scale: float = 1.0) -> np.ndarray:
    rows, cols = img.shape[:2]
    center = (cols / 2, rows / 2)
    M = cv2.getRotationMatrix2D(center, angle, scale)
    return cv2.warpAffine(img, M, (cols, rows))


def apply_operation(img: np.ndarray, op: str, params: dict) -> np.ndarray:
    """
    Aplica una única operación según 'op' y parámetros en 'params'.
    """
    if op == 'rescale':
        fx = float(params.get('fx', 1.0))
        fy = float(params.get('fy', 1.0))
        return rescale(img, fx, fy)

    if op == 'histogram':
        return histogram(img, draw=True)

    if op == 'equalize':
        return equalize(img)

    if op == 'linear_filter':
        k = int(params.get('kernel_size', 5))
        return linear_filter(img, k)

    if op == 'nonlinear_filter':
        k = int(params.get('ksize', 5))
        return nonlinear_filter(img, k)

    if op == 'translate':
        tx = float(params.get('tx', 0))
        ty = float(params.get('ty', 0))
        return translate(img, tx, ty)

    if op == 'rotate':
        angle = float(params.get('angle', 0))
        scale = float(params.get('scale', 1.0))
        return rotate(img, angle, scale)

    # Si la operación no existe, retorna la original
    return img


def apply_operations(img: np.ndarray, operations: list, params: dict) -> np.ndarray:
    """
    Aplica en secuencia todas las operaciones listadas en 'operations',
    usando los mismos 'params' para cada llamada a apply_operation.
    :param img: imagen BGR de entrada.
    :param operations: lista de nombres de operaciones a aplicar en orden.
    :param params: diccionario con parámetros para cada operación.
    :return: imagen procesada tras aplicar todas las operaciones.
    """
    output = img.copy()
    for op in operations:
        output = apply_operation(output, op, params)
    return output
