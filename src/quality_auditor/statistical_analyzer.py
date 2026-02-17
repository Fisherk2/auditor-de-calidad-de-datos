"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Análisis estadístico
AUTOR:       Fisherk2
FECHA:       2026-02-17
DESCRIPCIÓN: Proporciona funciones para resumen estadístico (min, max, promedio) solo para numéricas
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""
import math
from typing import Any
from src.utils.data_parser import DataParser

# ⋮⋮⋮⋮⋮⋮⋮⋮ ALIAS de estructura datos ⋮⋮⋮⋮⋮⋮⋮⋮
RowDataType = list[dict[str, Any]]
MetricDataType = dict[str, dict[str, float]]
ValueListType = dict[str, list[float]]


class StatisticalAnalyzer:
    """
    Clase para análisis estadístico de datos numéricos en estructuras de datos
    """

    @staticmethod
    def summary_stadistic(data: RowDataType) -> MetricDataType:
        """
        Calcula metricas estadisticas basicas para columnas numericas
        :param data: Lista de diccionarios representando filas de datos
        :return: Diccionario con nombre de columna como clave y métricas estadísticas como valor:
        ["minimum", "maximum", "average", "sum", "count", "standard_deviation"]
        """
        if data is None or not data:
            return dict()

        # ■■■■■■■■■■■■■ Obtener todas las columnas posibles ■■■■■■■■■■■■■
        all_columns = set()
        for row in data:
            for column in row.keys():
                all_columns.add(column)

        results = dict()

        for column in all_columns:
            numeric_values = list()

            # ▲▲▲▲▲▲ Recoger valores numericos de la columna ▲▲▲▲▲▲
            for row in data:
                if column in row.keys():
                    value = row[column]
                    if DataParser.is_numeric_value(value):
                        numeric_values.append(float(value))

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

                # ▲▲▲▲▲▲ Guardar resultados ▲▲▲▲▲▲
                stadistics["minimum"] = round(minimum, 2)
                stadistics["maximum"] = round(maximum, 2)
                stadistics["average"] = round(average, 2)
                stadistics["sum"] = round(suma, 2)
                stadistics["count"] = count
                stadistics["standard_deviation"] = round(standard_deviation, 2)

                results[column] = stadistics

        return results

    @staticmethod
    def count_by_type(data: RowDataType) -> dict[str, int]:
        """
        Cuenta cuantas columnas son numericas, de texto, booleanas, etc.
        :param data: Lista de diccionarios representando filas de datos
        :return: Diccionario con categorias de tipo y conteo de columnas:
        ["numerics", "texts", "booleans", "others"]
        """
        if data is None or not data:
            return dict()

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
                    count_total = 0

                    if DataParser.is_numeric_value(value):
                        count_numeric += 1
                    elif DataParser.is_string_value(value):
                        count_text += 1
                    elif DataParser.is_bool_value(value):
                        count_booleans += 1

            # ▲▲▲▲▲▲ Determinar tipo predominante (más del 50% ▲▲▲▲▲▲
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
    def get_numerics_values(data: RowDataType) -> ValueListType:
        """
        Extrae solo los valores numericos por columna
        :param data: Lista de diccionarios representando filas de datos
        :return: Diccionario con nombre de la columna como clave y lista de valores numericos como valor
        """
        if data is None or not data:
            return dict()

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
                    if DataParser.is_numeric_value(value):
                        numeric_list.append(float(value))

            if numeric_list:
                numerics_values[column] = numeric_list

        return numerics_values