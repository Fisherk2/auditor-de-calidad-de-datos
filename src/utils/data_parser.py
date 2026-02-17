"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Parseo y validación básica de datos de entrada
AUTOR:       Fisherk2
FECHA:       2026-02-16
DESCRIPCIÓN: Capa de acceso a datos que proporciona funciones para validar y transformar datos de entrada
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""

from typing import Any, Optional
import re

# ⋮⋮⋮⋮⋮⋮⋮⋮ ALIAS de estructura datos ⋮⋮⋮⋮⋮⋮⋮⋮
RowDataType = list[dict[str, Any]]
ColumnIndexMap = dict[str, list[int]]

class DataParser:
    """
    Clase de utilidad para parseo y validación de datos estructurados
    """

    @staticmethod
    def is_numeric_value(value:Any) -> bool:
        """
        Verifica si un valor puede ser convertido a número
        :param value:
        :return: ¿Es un valor numérico?
        """
        if value == None:
            return False
        if isinstance(value, (int, float)): # TODO: Verificar como saber si una instancia es numero entero
            return True
        if isinstance(value,str):
            try:
                float(value)
                return True
            except ValueError:
                return False
        return False

    @staticmethod
    def is_string_value(value:Any) -> bool:
        """
        Verifica si un valor es una cadena valida (no vacia)
        :param value:
        :return: ¿Es una cadena valida?
        """
        if value == None:
            return False
        if isinstance(value,str):
            return value.strip().length() > 0
        return False

    @staticmethod
    def is_bool_value(value:Any) -> bool:
        """
        Verifica si un valor puede ser interpretado como booleano
        :param value:
        :return: ¿Es un valor booleano?
        """
        if value == None:
            return False
        if isinstance(value,bool):
            return True
        if isinstance(value,str):
            lower_value = value.lower().strip()

            # TODO: ▁▂▃▄▅▆▇███████ Interpretaciones aceptadas ███████▇▆▅▄▃▂▁
            return (
                    lower_value == "true" or lower_value == "false" or
                    lower_value == "1" or lower_value == "0" or
                    lower_value == "yes" or lower_value == "no" or
                    lower_value == "on" or lower_value == "off"
            )

        return False

    @staticmethod
    def is_null_value(value:Any) -> bool:
        """
        Verifica si un valor es nulo o representa un valor nulo
        :param value:
        :return: ¿Es un valor nulo?
        """
        if value == None:
            return True
        if isinstance(value,str):
            trimmed = value.lower().strip()

            # TODO: ▁▂▃▄▅▆▇███████ Interpretaciones aceptadas ███████▇▆▅▄▃▂▁
            return (
                trimmed == "" or trimmed == "null" or
                trimmed == "none" or trimmed == "na" or
                trimmed == "n/a" or trimmed == "<null>"
            )

        return False

    @staticmethod
    def get_column_index(data: RowDataType) -> ColumnIndexMap:
        """
        Obtiene los indices de aparicion de cada columna de los datos
        para recibir una lista de diccionarios (que representan filas de datos)
        y devolver un diccionario que mapea cada nombre de columna
        a una lista de los índices (posiciones) de las filas en las que
        esa columna aparece.
        :return: Diccionario de indices de cada columna
        """
        if not data:
            return dict()

        # ■■■■■■■■■■■■■ Obtenemos la primera fila de datos para conocer las columnas existentes ■■■■■■■■■■■■■
        column_index = dict()
        first_row = data[0]

        # ■■■■■■■■■■■■■ Iteramos sobre cada clave (nombre de columna) en la primera fila ■■■■■■■■■■■■■
        for key in first_row.keys():
            indexes = list()

            # ■■■■■■■■■■■■■ Recorremos cada fila en los datos (usando su índice) ■■■■■■■■■■■■■
            for i in range(len(data)):
                if key in data[i]:
                    indexes.append(i)

            # ■■■■■■■■■■■■■ Una vez recorridas todas las filas, asignamos la lista de índices al nombre de la columna ■■■■■■■■■■■■■
            column_index[key] = indexes

        return column_index

    @staticmethod
    def validate_row_structure(row:dict[str,Any], expected_columns:set[str]) -> dict[str,Any]:
        """
        Valida la estructura de una fila contra columnas esperadas
        :return: Diccionario de resultados que validan la fila
        """
        result = dict()
        result["valid"] = True
        result["missing_columns"] = list()
        result["extra_columns"] = list()

        # ■■■■■■■■■■■■■ Verificar columnas faltantes ■■■■■■■■■■■■■
        for expected_column in expected_columns:
            if not expected_column in row.keys():
                result["missing_columns"].append(expected_column)

        # ■■■■■■■■■■■■■ Verificar columnas extra ■■■■■■■■■■■■■
        for actual_column in row.keys():
            if not actual_column in expected_columns:
                result["extra_columns"].append(actual_column)

        has_issues = result["missing_columns"] or result["extra_columns"]
        result["valid"] = not has_issues

        return result


    # ▼△▼△▼△▼△▼△▼△▼△▼△▼△ Pseudocodigo △▼△▼△▼△▼△▼△▼△▼△▼△▼

public
static
List[Dict[String, Any]]
filterValidRows(List[Dict[String, Any]]
data, Set[String]
expectedColumns)
"""
Filtra filas que contienen todas las columnas esperadas
"""
var
validRows = list()
for Dict[String, Any] row in data
    var
    validation = DataParser.validateRowStructure(row, expectedColumns)
    if validation["valid"]
        validRows.append(row)
return validRows
