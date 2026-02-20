"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Análisis de unicidad
AUTOR:       Fisherk2
FECHA:       2026-02-17
DESCRIPCIÓN: Proporciona funciones para calcular porcentaje de valores únicos por columna
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""
from typing import Any, Optional
from collections import Counter
from src.readers.quality_rules_reader import QualityRulesReader

# ⋮⋮⋮⋮⋮⋮⋮⋮ ALIAS de estructura datos ⋮⋮⋮⋮⋮⋮⋮⋮
RowDataType = list[dict[str, Any]]
MetricValuesType = dict[str, dict[str, int]]
UniquenessResultType = dict[str, dict[str, Any]]


class UniquenessAnalyzer:
    """
    Clase para análisis de unicidad de valores en datos estructurados
    """

    @staticmethod
    def calculate_uniqueness(datos: RowDataType, path_quality_rules: Optional[str] = None) -> UniquenessResultType:
        """
        Calcula el porcentaje de valores únicos por columna con clasificación basada en configuración
        El porcentaje se calcula como: (número de valores únicos / número total de valores) * 100
        La clasificación se basa en umbrales de configuración: 'baja', 'normal', o 'alta'
        :param datos: Lista de diccionarios representando filas de datos
        :param path_quality_rules: Ruta opcional al archivo YAML de configuración
        :return: Diccionario extendido con unicidad y clasificación por columna
        """
        if datos is None or not datos:
            return dict()

        # ■■■■■■■■■■■■■ Cargar umbrales de configuración ■■■■■■■■■■■■■
        thresholds = UniquenessAnalyzer._get_uniqueness_thresholds(path_quality_rules)

        # ■■■■■■■■■■■■■ Obtener todas las columnas posibles ■■■■■■■■■■■■■
        all_columns = set()
        for row in datos:
            for column in row.keys():
                all_columns.add(column)

        unique_result = dict()

        for column in all_columns:
            values = list()

            # ▲▲▲▲▲▲ Recoger todos los valores de la columna ▲▲▲▲▲▲
            for row in datos:
                if column in row.keys():
                    values.append(row[column])

            # ▲▲▲▲▲▲ Salta a la siguiente columna si no hay valores ▲▲▲▲▲▲
            if not values:
                unique_result[column] = {
                    'uniqueness_percentage': 0.0,
                    'classification': 'normal',
                    'unique_values': 0,
                    'total_values': 0
                }
                continue

            # ▲▲▲▲▲▲ Contar frecuencia de cada valor ▲▲▲▲▲▲
            counter = Counter(values)

            # ▲▲▲▲▲▲ Contar valores que solo aparecen una sola vez ▲▲▲▲▲▲
            unique_values = 0
            for count in counter.values():
                if count == 1:
                    unique_values += 1

            # ▁▂▃▄▅▆▇███████ Calculo de porcentaje de unicidad ███████▇▆▅▄▃▂▁
            total_values = len(values)
            unique_percent = (unique_values / total_values) * 100.0
            unique_percent_rounded = round(unique_percent, 2)

            # ▲▲▲▲▲▲ Clasificar según umbrales ▲▲▲▲▲▲
            classification = UniquenessAnalyzer._classify_uniqueness(unique_percent_rounded, thresholds)

            unique_result[column] = {
                'uniqueness_percentage': unique_percent_rounded,
                'classification': classification,
                'unique_values': unique_values,
                'total_values': total_values
            }

        return unique_result

    @staticmethod
    def get_unique_details(datos: RowDataType) -> MetricValuesType:
        """
        Obtiene detalles adicionales sobre unicidad: conteo de únicos, duplicados y total por columna
        :param datos: Lista de diccionarios representando filas de datos
        :return: Diccionario con nombre de columna como clave y diccionario de metricas como valor
        """
        if datos is None or not datos:
            return dict()

        # ■■■■■■■■■■■■■ Obtener todas las columnas posibles ■■■■■■■■■■■■■
        all_columns = set()
        for row in datos:
            for column in row.keys():
                all_columns.add(column)

        details = dict()
        for column in all_columns:

            # ▲▲▲▲▲▲ Recoger todos los valores de la columna ▲▲▲▲▲▲
            values = list()
            for row in datos:
                if column in row.keys():
                    values.append(row[column])

            # ▲▲▲▲▲▲ Salta a la siguiente columna si no hay valores ▲▲▲▲▲▲
            if not values:
                details[column] = dict()
                details[column]["total"] = 0
                details[column]["unicos"] = 0
                details[column]["duplicados"] = 0
                details[column]["porcentajeUnicidad"] = 0.0
                continue

            # ▲▲▲▲▲▲ Contar frecuencia de cada valor ▲▲▲▲▲▲
            counter = Counter(values)
            total = len(counter)
            uniques = 0
            duplicates = 0

            for count in counter.values():
                if count == 1:
                    uniques += 1
                else:
                    duplicates += count

            details[column] = dict()
            details[column]["total"] = total
            details[column]["unicos"] = uniques
            details[column]["duplicados"] = duplicates
            details[column]["porcentajeUnicidad"] = round((uniques / total) * 100.0, 2)

        return details

    @staticmethod
    def _get_uniqueness_thresholds(path_quality_rules: Optional[str]) -> dict[str, float]:
        """
        Obtiene los umbrales de unicidad desde configuración o valores por defecto
        :param path_quality_rules: Ruta opcional al archivo YAML de configuración
        :return: Diccionario con umbrales min y max
        """
        if path_quality_rules:
            try:
                config = QualityRulesReader.load_configs(path_quality_rules)
                general_rules = QualityRulesReader.get_general_rules(config)
                return {
                    'min_uniqueness_percentage': general_rules.get('min_uniqueness_percentage', 5.0),
                    'max_uniqueness_percentage': general_rules.get('max_uniqueness_percentage', 95.0)
                }
            except (FileNotFoundError, ValueError, Exception):
                # ■■■■■■■■■■■■■ Si hay error, usar valores por defecto ■■■■■■■■■■■■■
                pass

        # ■■■■■■■■■■■■■ Valores por defecto si no hay configuración ■■■■■■■■■■■■■
        default_config = QualityRulesReader.apply_default_rules()
        general_rules = QualityRulesReader.get_general_rules(default_config)
        return {
            'min_uniqueness_percentage': general_rules.get('min_uniqueness_percentage', 5.0),
            'max_uniqueness_percentage': general_rules.get('max_uniqueness_percentage', 95.0)
        }

    @staticmethod
    def _classify_uniqueness(percentage: float, thresholds: dict[str, float]) -> str:
        """
        Clasifica el porcentaje de unicidad según umbrales
        :param percentage: Porcentaje de unicidad
        :param thresholds: Umbrales min y max
        :return: Clasificación: 'baja', 'normal', o 'alta'
        """
        min_threshold = thresholds.get('min_uniqueness_percentage', 5.0)
        max_threshold = thresholds.get('max_uniqueness_percentage', 95.0)

        if percentage < min_threshold:
            return 'baja'
        elif percentage > max_threshold:
            return 'alta'
        else:
            return 'normal'
