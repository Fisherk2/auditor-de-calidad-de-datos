"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Análisis de nulos
AUTOR:       Fisherk2
FECHA:       2026-02-17
DESCRIPCIÓN: Proporciona función para contar valores nulos por columna
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""

from typing import Any, Optional
from src.utils.data_parser import DataParser
from src.readers.quality_rules_reader import QualityRulesReader

# ⋮⋮⋮⋮⋮⋮⋮⋮ ALIAS de estructura datos ⋮⋮⋮⋮⋮⋮⋮⋮
RowDataType = list[dict[str, Any]]

class NullAnalyzer:
    """
    Clase para análisis de valores nulos en datos estructurados
    """

    @staticmethod
    def count_nulls(datos: RowDataType, path_quality_rules: Optional[str] = None) -> dict[str, int]:
        """
        Calcula el conteo de valores nulos por columna en una lista de diccionarios
        Un valor se considera nulo según las reglas de configuración o valores por defecto
        :param datos: Lista de diccionarios representando filas de datos
        :param path_quality_rules: Ruta opcional al archivo YAML de configuración
        :return: Diccionario con nombre de columna como clave y conteo de nulos como valor
        """
        if datos is None or not datos:
            return dict()

        # ■■■■■■■■■■■■■ Cargar configuración de nulos ■■■■■■■■■■■■■
        null_rules = NullAnalyzer._get_null_rules(path_quality_rules)

        # ■■■■■■■■■■■■■ Obtener todas las columnas posibles ■■■■■■■■■■■■■
        all_columns = set()
        for fila in datos:
            for column in fila.keys():
                all_columns.add(column)

        # ■■■■■■■■■■■■■ Inicializar contador de nulos ■■■■■■■■■■■■■
        nulls = dict()
        for column in all_columns:
            nulls[column] = 0

        # ■■■■■■■■■■■■■ Contar nulos columna por columna ■■■■■■■■■■■■■
        for fila in datos:
            for column in all_columns:
                value = fila.get(column, None)
                if DataParser.is_null_value(value, null_rules):
                    nulls[column] += 1

        return nulls

    @staticmethod
    def _get_null_rules(path_quality_rules: Optional[str]) -> dict[str, Any]:
        """
        Obtiene las reglas de nulos desde configuración o valores por defecto
        :param path_quality_rules: Ruta opcional al archivo YAML de configuración
        :return: Diccionario con reglas de nulos
        """
        if path_quality_rules:
            try:
                config = QualityRulesReader.load_configs(path_quality_rules)
                return QualityRulesReader.get_data_type_rules(config, 'null')
            except (FileNotFoundError, ValueError, Exception):
                # ■■■■■■■■■■■■■ Si hay error, usar valores por defecto ■■■■■■■■■■■■■
                pass
        
        # ■■■■■■■■■■■■■ Valores por defecto si no hay configuración ■■■■■■■■■■■■■
        default_config = QualityRulesReader.apply_default_rules()
        return QualityRulesReader.get_data_type_rules(default_config, 'null')