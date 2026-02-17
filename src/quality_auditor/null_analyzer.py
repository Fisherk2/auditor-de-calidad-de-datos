"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Análisis de nulos
AUTOR:       Fisherk2
FECHA:       2026-02-17
DESCRIPCIÓN: Proporciona función para contar valores nulos por columna
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""

from typing import Any
from src.utils.data_parser import DataParser

# ⋮⋮⋮⋮⋮⋮⋮⋮ ALIAS de estructura datos ⋮⋮⋮⋮⋮⋮⋮⋮
RowDataType = list[dict[str, Any]]

class NullAnalyzer:
    """
    Clase para análisis de valores nulos en datos estructurados
    """

    @staticmethod
    def count_nulls(datos: RowDataType) -> dict[str, int]:
        """
        Calcula el conteo de valores nulos por columna en una lista de diccionarios
        Un valor se considera nulo si es None, string vacío, 'null', 'none', 'na', 'n/a', '<null>'
        :param datos: Lista de diccionarios representando filas de datos
        :return: Diccionario con nombre de columna como clave y conteo de nulos como valor
        """
        if datos is None or not datos:
            return dict()

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
                if DataParser.is_null_value(value):
                    nulls[column] += 1

        return nulls