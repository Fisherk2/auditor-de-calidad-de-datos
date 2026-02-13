"""
Módulo src para el Validador de CSV para Pipelines de Datos
Este paquete contiene todos los componentes necesarios para validar archivos CSV
contra un esquema predefinido.
"""

# ▁▂▃▄▅▆▇███████ Versión del paquete ███████▇▆▅▄▃▂▁
__version__ = "1.0.0"
__author__ = "Fisherk2"

# ⋮⋮⋮⋮⋮⋮⋮⋮ Importar clases desde submódulos ⋮⋮⋮⋮⋮⋮⋮⋮
from src.validators.csv_validator import CSVValidator
from src.readers.csv_reader import CSVReader
from src.validators.type_validator import TypeValidator
from src.validators.schema_validator import SchemaValidator
from src.utils.error_reporter import ErrorReporter

# ⋮⋮⋮⋮⋮⋮⋮⋮ Declaración de módulos disponibles para importación ⋮⋮⋮⋮⋮⋮⋮⋮
__all__ = [
    'CSVValidator',
    'CSVReader',
    'TypeValidator',
    'SchemaValidator',
    'ErrorReporter'
]