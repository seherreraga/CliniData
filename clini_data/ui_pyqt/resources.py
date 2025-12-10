import os
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

# Ruta base relativa al paquete; asegúrate de que los assets estén en clini_data/assets/
BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "logo")

def resource_path(fname: str):
    """Devuelve la ruta filesystem al recurso dentro del paquete (relativa)."""
    return os.path.abspath(os.path.join(BASE_DIR, fname))

def get_pixmap(name: str, width: int = None, height: int = None, keep_aspect=True) -> QPixmap:
    """Carga una imagen y devuelve QPixmap escalada si width/height son provistos."""
    path = resource_path(name)
    pix = QPixmap(path)
    if pix.isNull():
        # fallback: pixmap vacío para evitar crashes
        return QPixmap()
    if width or height:
        if keep_aspect:
            return pix.scaled(width or pix.width(), height or pix.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            return pix.scaled(width or pix.width(), height or pix.height(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
    return pix

def app_icon(icon_name="logo_icon_64.png") -> QIcon:
    p = resource_path(icon_name)
    return QIcon(p) if os.path.exists(p) else QIcon()
