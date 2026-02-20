"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Análisis estadístico
AUTOR:       Fisherk2
FECHA:       2026-02-17
DESCRIPCIÓN: Proporciona funciones para resumen estadístico (min, max, promedio) solo para numéricas
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""
import math
from typing import Any, Optional
from utils.data_parser import DataParser
from readers.quality_rules_reader import QualityRulesReader

# ⋮⋮⋮⋮⋮⋮⋮⋮ ALIAS de estructura datos ⋮⋮⋮⋮⋮⋮⋮⋮
RowDataType = list[dict[str, Any]]
MetricDataType = dict[str, dict[str, float]]
ValueListType = dict[str, list[float]]


class StatisticalAnalyzer:
    """
    Clase para análisis estadístico de datos numéricos en estructuras de datos
    """

    @staticmethod
    def summary_stadistic(data: RowDataType, path_quality_rules: Optional[str] = None) -> dict[str, Any]:
        """
        Calcula metricas estadisticas basicas para columnas numericas usando configuración
        :param data: Lista de diccionarios representando filas de datos
        :param path_quality_rules: Ruta opcional al archivo YAML de configuración
        :return: Diccionario con estadísticas, valores fuera de rango y reglas aplicadas
        """
        if data is None or not data:
            return {"statistics": {}, "out_of_range": {}, "rules_applied": {}}

        # ■■■■■■■■■■■■ Cargar configuración de números ■■■■■■■■■■■■■
        numeric_rules = StatisticalAnalyzer._get_numeric_rules(path_quality_rules)
        precision = numeric_rules.get('precision', 2)
        min_value = numeric_rules.get('min_value')
        max_value = numeric_rules.get('max_value')
        allow_negative = numeric_rules.get('allow_negative', True)

        # ■■■■■■■■■■■■ Guardar reglas aplicadas ■■■■■■■■■■■■■
        rules_applied = {
            "precision": precision,
            "min_value": min_value,
            "max_value": max_value,
            "allow_negative": allow_negative
        }

        # ■■■■■■■■■■■■■ Obtener todas las columnas posibles ■■■■■■■■■■■■■
        all_columns = set()
        for row in data:
            for column in row.keys():
                all_columns.add(column)

        results = dict()
        out_of_range = dict()

        for column in all_columns:
            numeric_values = list()
            out_of_range_values = list()

            # ▲▲▲▲▲▲ Recoger valores numericos de la columna ▲▲▲▲▲▲
            for row in data:
                if column in row.keys():
                    value = row[column]
                    if DataParser.is_numeric_value(value, numeric_rules):
                        numeric_value = float(value)
                        numeric_values.append(numeric_value)

                        # ▲▲▲▲▲▲ Verificar si está fuera de rango ▲▲▲▲▲▲
                        if StatisticalAnalyzer._is_out_of_range(numeric_value, min_value, max_value):
                            out_of_range_values.append({
                                "row_index": data.index(row),
                                "value": numeric_value,
                                "reason": StatisticalAnalyzer._get_out_of_range_reason(numeric_value, min_value,
                                                                                       max_value)
                            })

            # ▁▂▃▄▅▆▇███████ Calculo de estadisticos ███████▇▆▅▄▃▂▁
            if numeric_values:
                stadistics = dict()

                # ▲▲▲▲▲▲ Calcular metricas basicas ▲▲▲▲▲▲
                minimum = numeric_values[0]
                maximum = numeric_values[0]
                suma = 0.0

                for number in numeric_values:
                    if number < minimum:
                        minimum = number
                    if number > maximum:
                        maximum = number
                    suma += number

                count = len(numeric_values)
                average = suma / count

                # ▲▲▲▲▲▲ Calcular desviacion estandar ▲▲▲▲▲▲
                squares_sum = 0.0
                for number in numeric_values:
                    difference = number - average
                    squares_sum += difference * difference

                # ▲▲▲▲▲▲ Calcular varianza muestral ▲▲▲▲▲▲
                variance = 0.0
                if count > 1:
                    variance = squares_sum / (count - 1)

                # ▲▲▲▲▲▲ Calcular desviación estandar ▲▲▲▲▲▲
                standard_deviation = math.sqrt(variance)

                # ▲▲▲▲▲▲ Guardar resultados con precisión configurada ▲▲▲▲▲▲
                stadistics["minimum"] = round(minimum, precision)
                stadistics["maximum"] = round(maximum, precision)
                stadistics["average"] = round(average, precision)
                stadistics["sum"] = round(suma, precision)
                stadistics["count"] = count
                stadistics["standard_deviation"] = round(standard_deviation, precision)

                # ▲▲▲▲▲▲ Agregar información adicional ▲▲▲▲▲▲
                stadistics["has_negatives"] = any(num < 0 for num in numeric_values)
                stadistics["negative_count"] = sum(1 for num in numeric_values if num < 0)

                results[column] = stadistics

                if out_of_range_values:
                    out_of_range[column] = out_of_range_values

        return {
            "statistics": results,
            "out_of_range": out_of_range,
            "rules_applied": rules_applied
        }

    @staticmethod
    def count_by_type(data: RowDataType, path_quality_rules: Optional[str] = None) -> dict[str, int]:
        """
        Cuenta cuantas columnas son numericas, de texto, booleanas, etc.
        :param data: Lista de diccionarios representando filas de datos
        :param path_quality_rules: Ruta opcional al archivo YAML de configuración
        :return: Diccionario con categorias de tipo y conteo de columnas:
        ["numerics", "texts", "booleans", "others"]
        """
        if data is None or not data:
            return dict()

        # ■■■■■■■■■■■■■ Obtener reglas de configuración ■■■■■■■■■■■■■
        all_rules = StatisticalAnalyzer._get_all_data_type_rules(path_quality_rules)
        numeric_rules = all_rules.get('numeric', {})
        text_rules = all_rules.get('text', {})
        boolean_rules = all_rules.get('boolean', {})

        # ■■■■■■■■■■■■■ Obtener todas las columnas posibles ■■■■■■■■■■■■■
        all_columns = set()
        for row in data:
            for column in row.keys():
                all_columns.add(column)

        count_types = dict()
        count_types["numerics"] = 0
        count_types["texts"] = 0
        count_types["booleans"] = 0
        count_types["others"] = 0

        # ■■■■■■■■■■■■■ Para cada columna, determinar el tipo predominante ■■■■■■■■■■■■■
        for column in all_columns:
            count_numeric = 0
            count_text = 0
            count_booleans = 0
            count_total = 0

            for row in data:
                if column in row.keys():
                    value = row[column]
                    count_total += 1

                    if DataParser.is_numeric_value(value, numeric_rules):
                        count_numeric += 1
                    elif DataParser.is_string_value(value, text_rules):
                        count_text += 1
                    elif DataParser.is_bool_value(value, boolean_rules):
                        count_booleans += 1

            # ▲▲▲▲▲▲ Determinar tipo predominante (más del 50%) ▲▲▲▲▲▲
            if count_total > 0:
                umbral = count_total / 2.0
                if count_numeric >= umbral:
                    count_types["numerics"] += 1
                elif count_text >= umbral:
                    count_types["texts"] += 1
                elif count_booleans >= umbral:
                    count_types["booleans"] += 1
                else:
                    count_types["others"] += 1

        return count_types

    @staticmethod
    def get_numerics_values(data: RowDataType, path_quality_rules: Optional[str] = None) -> ValueListType:
        """
        Extrae solo los valores numericos por columna
        :param data: Lista de diccionarios representando filas de datos
        :param path_quality_rules: Ruta opcional al archivo YAML de configuración
        :return: Diccionario con nombre de la columna como clave y lista de valores numericos como valor
        """
        if data is None or not data:
            return dict()

        # ■■■■■■■■■■■■■ Obtener reglas de configuración para números ■■■■■■■■■■■■■
        all_rules = StatisticalAnalyzer._get_all_data_type_rules(path_quality_rules)
        numeric_rules = all_rules.get('numeric', {})

        # ■■■■■■■■■■■■■ Obtener todas las columnas posibles ■■■■■■■■■■■■■
        all_columns = set()
        for row in data:
            for column in row.keys():
                all_columns.add(column)

        numerics_values = dict()
        for column in all_columns:
            numeric_list = list()

            for row in data:
                if column in row.keys():
                    value = row[column]
                    if DataParser.is_numeric_value(value, numeric_rules):
                        numeric_list.append(float(value))

            if numeric_list:
                numerics_values[column] = numeric_list

        return numerics_values

    @staticmethod
    def _get_numeric_rules(path_quality_rules: Optional[str]) -> dict[str, Any]:
        """
        Obtiene las reglas de números desde configuración o valores por defecto
        :param path_quality_rules: Ruta opcional al archivo YAML de configuración
        :return: Diccionario con reglas de números
        """
        if path_quality_rules:
            try:
                config = QualityRulesReader.load_configs(path_quality_rules)
                return QualityRulesReader.get_data_type_rules(config, 'numeric')
            except (FileNotFoundError, ValueError, Exception):

                # ■■■■■■■■■■■■■ Si hay error, usar valores por defecto ■■■■■■■■■■■■■
                pass

        # ■■■■■■■■■■■■■ Valores por defecto si no hay configuración ■■■■■■■■■■■■■
        default_config = QualityRulesReader.apply_default_rules()
        return QualityRulesReader.get_data_type_rules(default_config, 'numeric')

    @staticmethod
    def _is_out_of_range(value: float, min_value: Optional[float], max_value: Optional[float]) -> bool:
        """
        Verifica si un valor está fuera del rango configurado
        :param value: Valor a verificar
        :param min_value: Valor mínimo permitido
        :param max_value: Valor máximo permitido
        :return: ¿Está fuera de rango?
        """
        if min_value is not None and value < min_value:
            return True
        if max_value is not None and value > max_value:
            return True
        return False

    @staticmethod
    def _get_out_of_range_reason(value: float, min_value: Optional[float], max_value: Optional[float]) -> str:
        """
        Determina la razón por la que un valor está fuera de rango
        :param value: Valor fuera de rango
        :param min_value: Valor mínimo permitido
        :param max_value: Valor máximo permitido
        :return: Razón del error
        """
        if min_value is not None and value < min_value:
            return f"below minimum ({min_value})"
        if max_value is not None and value > max_value:
            return f"above maximum ({max_value})"
        return "unknown"

    @staticmethod
    def _get_all_data_type_rules(path_quality_rules: Optional[str] = None) -> dict[str, dict[str, Any]]:
        """
        Obtiene todas las reglas de tipos de datos desde configuración o valores por defecto
        :param path_quality_rules: Ruta opcional al archivo YAML de configuración
        :return: Diccionario con reglas para cada tipo de dato
        """
        if path_quality_rules:
            try:
                config = QualityRulesReader.load_configs(path_quality_rules)
                data_type_rules = config.get('quality_rules', {}).get('data_type_rules', {})
                return data_type_rules
            except (FileNotFoundError, ValueError, Exception):

                # ■■■■■■■■■■■■■ Si hay error, usar valores por defecto ■■■■■■■■■■■■■
                pass

        # ■■■■■■■■■■■■■ Valores por defecto si no hay configuración ■■■■■■■■■■■■■
        default_config = QualityRulesReader.apply_default_rules()
        return default_config.get('quality_rules', {}).get('data_type_rules', {})
