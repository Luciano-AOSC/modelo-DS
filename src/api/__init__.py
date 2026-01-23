"""
Paquete de la API y entrypoint único de la app.
"""

from .app import create_app

app = create_app()
