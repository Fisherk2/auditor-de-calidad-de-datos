"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Análisis de unicidad
AUTOR:       Fisherk2
FECHA:       2026-02-17
DESCRIPCIÓN: Proporcionar función para calcular porcentaje de valores únicos por columna
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""
from typing import List, Dict, Any
from collections import Counter

# ⋮⋮⋮⋮⋮⋮⋮⋮ ALIAS de estructura datos ⋮⋮⋮⋮⋮⋮⋮⋮
RowDataType = list[dict[str, Any]]


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

    # ▼△▼△▼△▼△▼△▼△▼△▼△▼△ Pseudocodigo △▼△▼△▼△▼△▼△▼△▼△▼△▼

public
static
Dict[String, Dict[String, int]]
obtenerDetallesUnicidad(List[Dict[String, Any]]
datos)
"""
Obtiene detalles adicionales sobre unicidad: conteo de únicos, duplicados y total por columna

Args:
    datos: Lista de diccionarios representando filas de datos

Returns:
    Diccionario con nombre de columna como clave y diccionario de métricas como valor
"""
if datos == null | | datos.isEmpty()
    return dict()

var
todasLasColumnas = set()
for Dict[String, Any] fila in datos
    for String columna in fila.keySet()
        todasLasColumnas.add(columna)

var
detalles = dict()

for String columna in todasLasColumnas
    var
    valores = list()
    for Dict[String, Any] fila in datos
        if fila.containsKey(columna)
            valores.append(fila[columna])

    if valores.isEmpty()
        detalles[columna] = dict()
        detalles[columna]["total"] = 0
        detalles[columna]["unicos"] = 0
        detalles[columna]["duplicados"] = 0
        detalles[columna]["porcentajeUnicidad"] = 0.0
        continue

    var
    contador = Counter(valores)
    var
    total = valores.size()
    var
    unicos = 0
    var
    duplicados = 0

    for var count in contador.values()
        if count == 1
            unicos + +
        else
            duplicados += count

    detalles[columna] = dict()
    detalles[columna]["total"] = total
    detalles[columna]["unicos"] = unicos
    detalles[columna]["duplicados"] = duplicados
    detalles[columna]["porcentajeUnicidad"] = round((unicos / total) * 100.0, 2)

return detalles
