#!/usr/bin/env python3
"""
Archivo de inicio para Render - maneja el puerto dinámico
"""
import os
import sys

# Configurar el puerto para Render
if 'PORT' in os.environ:
    port = int(os.environ['PORT'])
    # Actualizar la configuración del puerto
    os.environ['WEB_PORT'] = str(port)

# Importar y ejecutar la aplicación principal
if __name__ == "__main__":
    import main