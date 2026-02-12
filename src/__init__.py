"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Init
AUTOR:       Fisherk2
FECHA:       2026-02-11
DESCRIPCIÓN: Package initialization for CSV Validator components
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""

# Versión del paquete
__version__ = "1.0.0"

# Exportar componentes principales
from .validators import CSVValidator
from .readers import CSVReader

# Definir qué se importa con "from package import *"
__all__ = ["CSVValidator", "CSVReader"]
