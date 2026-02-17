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
        if isinstance(value, (int,float)):
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

    # ▼△▼△▼△▼△▼△▼△▼△▼△▼△ Pseudocodigo △▼△▼△▼△▼△▼△▼△▼△▼△▼

public
static
Dict[String, List[int]]
getColumnIndices(List[Dict[String, Any]]
data)
"""
Obtiene los índices de aparición de cada columna en los datos
"""
if data.isEmpty()
    return dict()

var
columnIndices = dict()
var
firstRow = data[0]

for String key in firstRow.keySet()
    var
    indices = list()
    for int i = 0; i < data.size(); i++
    if data[i].containsKey(key)
        indices.append(i)
columnIndices[key] = indices

return columnIndices

public
static
Dict[String, Any]
validateRowStructure(Dict[String, Any]
row, Set[String]
expectedColumns)
"""
Valida la estructura de una fila contra columnas esperadas
"""
var
result = dict()
result["valid"] = true
result["missing_columns"] = list()
result["extra_columns"] = list()

# Verificar columnas faltantes
for String expectedCol in expectedColumns
    if !row.containsKey(expectedCol)
    result["missing_columns"].append(expectedCol)

# Verificar columnas extra
for String actualCol in row.keySet()
    if !expectedColumns.contains(actualCol)
    result["extra_columns"].append(actualCol)

result["valid"] = result["missing_columns"].isEmpty() & & result["extra_columns"].isEmpty()
return result

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
