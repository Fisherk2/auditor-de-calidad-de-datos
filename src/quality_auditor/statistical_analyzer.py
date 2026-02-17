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
from src.utils.data_parser import DataParser

# ⋮⋮⋮⋮⋮⋮⋮⋮ ALIAS de estructura datos ⋮⋮⋮⋮⋮⋮⋮⋮
RowDataType = list[dict[str, Any]]
MetricDataType = dict[str, dict[str, float]]

class StatisticalAnalyzer:
    """
    Clase para análisis estadístico de datos numéricos en estructuras de datos
    """

    @staticmethod
    def summary_stadistic(data:RowDataType) -> MetricDataType:
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
                sum = 0.0

                for number in numeric_values:
                    if number < minimum:
                        minimum = number
                    if number > maximum:
                        maximum = number
                    sum += number

                count = len(numeric_values)
                average = sum / count

                # ▲▲▲▲▲▲ Calcular desviacion estandar ▲▲▲▲▲▲
                squares_sum = 0.0
                for number in numeric_values:
                    difference = number - average
                    squares_sum += difference*difference

                # ▲▲▲▲▲▲ Calcular varianza muestral ▲▲▲▲▲▲
                variance = 0.0
                if count > 1:
                    variance = squares_sum / (count -1)

                # ▲▲▲▲▲▲ Calcular desviación estandar ▲▲▲▲▲▲
                standard_deviation = math.sqrt(variance)

                # ▲▲▲▲▲▲ Guardar resultados ▲▲▲▲▲▲
                stadistics["minimum"] = round(minimum, 2)
                stadistics["maximum"] = round(maximum, 2)
                stadistics["average"] = round(average, 2)
                stadistics["sum"] = round(sum, 2)
                stadistics["count"] = count
                stadistics["standard_deviation"] = round(standard_deviation, 2)

                results[column] = stadistics

        return results


# ▼△▼△▼△▼△▼△▼△▼△▼△▼△ Pseudocodigo △▼△▼△▼△▼△▼△▼△▼△▼△▼

public
static
Dict[String, int]
conteoPorTipo(List[Dict[String, Any]]
datos)
"""
Cuenta cuántas columnas son numéricas, de texto, booleanas, etc.

Args:
    datos: Lista de diccionarios representando filas de datos

Returns:
    Diccionario con categorías de tipo y conteo de columnas
"""
if datos == null | | datos.isEmpty()
    return dict()

var
todasLasColumnas = set()
for Dict[String, Any] fila in datos
    for String columna in fila.keySet()
        todasLasColumnas.add(columna)

var
conteoTipos = dict()
conteoTipos["numericas"] = 0
conteoTipos["texto"] = 0
conteoTipos["booleanas"] = 0
conteoTipos["otras"] = 0

# Para cada columna, determinar el tipo predominante
for String columna in todasLasColumnas
    var
    conteoNumericos = 0
    var
    conteoTexto = 0
    var
    conteoBooleanos = 0
    var
    conteoTotal = 0

    for Dict[String, Any] fila in datos
        if fila.containsKey(columna)
            var
            valor = fila[columna]
            conteoTotal + +

            if DataParser.isNumericValue(valor)
                conteoNumericos + +
            elif DataParser.isStringValue(valor)
                conteoTexto + +
            elif DataParser.isBooleanValue(valor)
                conteoBooleanos + +

    # Determinar tipo predominante (más del 50%)
    if conteoTotal > 0
        var
        umbral = conteoTotal / 2.0
        if conteoNumericos >= umbral
            conteoTipos["numericas"] + +
        elif conteoTexto >= umbral
            conteoTipos["texto"] + +
        elif conteoBooleanos >= umbral
            conteoTipos["booleanas"] + +
        else
            conteoTipos["otras"] + +

return conteoTipos

public
static
Dict[String, List[float]]
obtenerValoresNumericos(List[Dict[String, Any]]
datos)
"""
Extrae solo los valores numéricos por columna

Args:
    datos: Lista de diccionarios representando filas de datos

Returns:
    Diccionario con nombre de columna como clave y lista de valores numéricos como valor
"""
if datos == null | | datos.isEmpty()
    return dict()

var
todasLasColumnas = set()
for Dict[String, Any] fila in datos
    for String columna in fila.keySet()
        todasLasColumnas.add(columna)

var
valoresNumericos = dict()

for String columna in todasLasColumnas
    var
    listaNumerica = list()

    for Dict[String, Any] fila in datos
        if fila.containsKey(columna)
            var
            valor = fila[columna]
            if DataParser.isNumericValue(valor)
                listaNumerica.append(float(valor))

    if !listaNumerica.isEmpty()
    valoresNumericos[columna] = listaNumerica

return valoresNumericos