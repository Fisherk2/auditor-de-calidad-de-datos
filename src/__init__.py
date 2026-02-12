"""
Módulo src para el Validador de CSV para Pipelines de Datos
Este paquete contiene todos los componentes necesarios para validar archivos CSV
contra un esquema predefinido.
"""

# ▁▂▃▄▅▆▇███████ Versión del paquete ███████▇▆▅▄▃▂▁ #
__version__ = "1.0.0"
__author__ = "Fisherk2"

# ⋮⋮⋮⋮⋮⋮⋮⋮ Declaración de módulos disponibles para importación ⋮⋮⋮⋮⋮⋮⋮⋮ #
__all__ = [
    'CSVValidator',
    'CSVReader',
    'TypeValidator',
    'SchemaValidator',
    'ErrorReporter'
]