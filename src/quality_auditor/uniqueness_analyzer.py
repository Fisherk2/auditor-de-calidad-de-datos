"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Análisis de unicidad
AUTOR:       Fisherk2
FECHA:       2026-02-17
DESCRIPCIÓN: Proporcionar función para calcular porcentaje de valores únicos por columna
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""
from typing import Any
from collections import Counter

# ⋮⋮⋮⋮⋮⋮⋮⋮ ALIAS de estructura datos ⋮⋮⋮⋮⋮⋮⋮⋮
RowDataType = list[dict[str, Any]]
MetricValuesType = dict[str, dict[str, int]]


class UniquenessAnalyzer:
    """
    Clase para análisis de unicidad de valores en datos estructurados
    """

    @staticmethod
    def calcular_unicidad(datos: RowDataType) -> dict[str, float]:
        """
        Calcula el porcentaje de valores únicos por columna en una lista de diccionarios
        El porcentaje se calcula como: (número de valores únicos / número total de valores) * 100
        :param datos: Lista de diccionarios representando filas de datos
        :return: Diccionario con nombre de columna como clave y porcentaje de unicidad como valor
        """
        if datos is None or not datos:
            return dict()

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
                unique_result[column] = 0.0
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
            unique_result[column] = round(unique_percent, 2)

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
