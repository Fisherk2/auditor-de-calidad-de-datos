"""
Módulo src para el Validador de CSV y Auditor de Calidad de Datos
Este paquete contiene todos los componentes necesarios para validar archivos CSV
contra un esquema predefinido y realizar análisis de calidad de datos.
"""

# ▁▂▃▄▅▆▇███████ Versión del paquete ███████▇▆▅▄▃▂▁
__version__ = "1.1.0"
__author__ = "Fisherk2"

# ⋮⋮⋮⋮⋮⋮⋮⋮ Importar clases desde submódulos ⋮⋮⋮⋮⋮⋮⋮⋮
from src.validators.csv_validator import CSVValidator
from src.readers.csv_reader import CSVReader
from src.validators.type_validator import TypeValidator
from src.validators.schema_validator import SchemaValidator
from src.utils.csv_error_reporter import CSVErrorReporter

from src.quality_auditor.main_auditor import QualityAuditor
from src.quality_auditor.null_analyzer import NullAnalyzer
from src.quality_auditor.uniqueness_analyzer import UniquenessAnalyzer
from src.quality_auditor.statistical_analyzer import StatisticalAnalyzer
from src.quality_auditor.date_analyzer import DateAnalyzer
from src.readers.quality_rules_reader import QualityRulesReader
from src.utils.quality_report import QualityReport
from src.utils.data_parser import DataParser
from src.utils.date_helper import DateHelper

# ⋮⋮⋮⋮⋮⋮⋮⋮ Declaración de módulos disponibles para importación ⋮⋮⋮⋮⋮⋮⋮⋮
__all__ = [
    'CSVValidator',
    'CSVReader',
    'TypeValidator',
    'SchemaValidator',
    'CSVErrorReporter',

    'QualityAuditor',
    'NullAnalyzer',
    'UniquenessAnalyzer',
    'StatisticalAnalyzer',
    'DateAnalyzer',
    'QualityRulesReader',
    'QualityReport',
    'DataParser',
    'DateHelper'
]