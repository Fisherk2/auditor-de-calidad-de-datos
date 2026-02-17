"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Análisis de fechas
AUTOR:       Fisherk2
FECHA:       2026-02-17
DESCRIPCIÓN: Proporciona funciones para verificar coherencia de fechas (ej: fecha_nacimiento > fecha_actual)
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""

from typing import Any
from datetime import datetime

from src.utils.error_reporter import ErrorReporter
from src.utils.date_helper import DateHelper

# ⋮⋮⋮⋮⋮⋮⋮⋮ ALIAS de estructura datos ⋮⋮⋮⋮⋮⋮⋮⋮
RowDataType = list[dict[str, Any]]

class DateAnalyzer:
    """
    Clase para análisis de coherencia y validación de fechas en datos estructurados
    """

    @staticmethod
    def check_date_coherence(datos:RowDataType, birth_column_name:str) -> list[str]:
        """
        Verifica la coherencia de fechas comparando contra la fecha actual
        Detecta fechas de nacimiento futuras o fechas imposibles
        :param datos: Lista de diccionarios representando filas de datos
        :param birth_column_name: Nombre de la columna que contiene fechas de nacimiento
        :return: Lista de mensajes de error indicando inconsistencias encontradas
        """
        if datos is None or not datos:
            return list()

        errors = list()

        if birth_column_name is None or not birth_column_name.strip():
            errors = list()
            errors.append("Error en encabezado: Nombre de columna de fecha inválido o vacío")
            return errors

        supported_formats = DateHelper.get_supported_formats()

        for i in range(len(datos)):
            row = datos[i]

            if not birth_column_name in row.keys():
                errors.append(f"Fila {str(i + 1)}: Columna '{birth_column_name}' no encontrada")
                continue

            # ■■■■■■■■■■■■■ Saltar valores nulos, el análisis de nulos se hace en otro módulo ■■■■■■■■■■■■■
            date_value = row[birth_column_name]
            if date_value is None:
                continue

            date:str = ""
            if isinstance(date_value,str):
                date:str = date_value.strip()
            else:
                date:str = str(date_value).strip()

            # ■■■■■■■■■■■■■ Saltar cadenas vacias ■■■■■■■■■■■■■
            if not date:
                continue

            # ■■■■■■■■■■■■■ Intentar parsear la fecha con diferentes formatos ■■■■■■■■■■■■■
            date_parsed = None
            for format in supported_formats:
                date_parsed = DateHelper.parse_date(date, format)
                if date_parsed is not None:
                    break

            if date_parsed is None:
                errors.append(f"Fila {i+1}: Fecha invalida en columna '{birth_column_name}': {date}")

            # ■■■■■■■■■■■■■ Verificar si la fecha es futura ■■■■■■■■■■■■■
            else:
                if DateHelper.is_future_date(date_parsed):
                    mensaje = f"""
                    Fila {i+1}: 
                    Fecha futura en columna '{birth_column_name}': {DateHelper.format_date(date_parsed, "%Y-%m-%d")} 
                    (actual: {DateHelper.format_date(datetime.now(), "%Y-%m-%d")})
                    """
                    errors.append(mensaje)

        return errors



    # ▼△▼△▼△▼△▼△▼△▼△▼△▼△ Pseudocodigo △▼△▼△▼△▼△▼△▼△▼△▼△▼

public
static
List[String]
verificarRangoFechas(List[Dict[String, Any]]
datos, String
nombreColumna,
Optional[datetime]
fechaMinima = null,
Optional[datetime]
fechaMaxima = null)
"""
Verifica que las fechas estén dentro de un rango específico

Args:
    datos: Lista de diccionarios representando filas de datos
    nombreColumna: Nombre de la columna que contiene las fechas
    fechaMinima: Fecha mínima permitida (opcional)
    fechaMaxima: Fecha máxima permitida (opcional)

Returns:
    Lista de mensajes de error indicando fechas fuera de rango
"""
if datos == null | | datos.isEmpty()
    return list()

if nombreColumna == null | | nombreColumna.trim().isEmpty()
    var
    errorList = list()
    errorList.append("Nombre de columna de fecha inválido o vacío")
    return errorList

var
errores = list()
var
formatosSoportados = DateHelper.getSupportedFormats()

for int i = 0; i < datos.size(); i++
var
fila = datos[i]

if !fila.containsKey(nombreColumna)
continue  # Saltar filas sin la columna

var
valorFecha = fila[nombreColumna]
if valorFecha == null
    continue  # Saltar valores nulos

var
fechaStr = ""
if isinstance(valorFecha, str)
    fechaStr = valorFecha.trim()
else
    fechaStr = str(valorFecha).trim()

if fechaStr.isEmpty()
    continue  # Saltar cadenas vacías

# Intentar parsear la fecha
var
fechaParseada = null
for String formato in formatosSoportados
    fechaParseada = DateHelper.parseDate(fechaStr, formato)
    if fechaParseada != null
        break

if fechaParseada != null
    # Verificar rango mínimo
    if fechaMinima != null & & DateHelper.isDateBefore(fechaParseada, fechaMinima)
        var
        mensaje = "Fila " + (i + 1) + ": Fecha fuera de rango mínimo en '" + nombreColumna + "': " + \
                  DateHelper.formatDate(fechaParseada, "%Y-%m-%d") + \
                  " (mínimo permitido: " + DateHelper.formatDate(fechaMinima, "%Y-%m-%d") + ")"
        errores.append(mensaje)

    # Verificar rango máximo
    if fechaMaxima != null & & DateHelper.isDateBefore(fechaMaxima, fechaParseada)
        var
        mensaje = "Fila " + (i + 1) + ": Fecha fuera de rango máximo en '" + nombreColumna + "': " + \
                  DateHelper.formatDate(fechaParseada, "%Y-%m-%d") + \
                  " (máximo permitido: " + DateHelper.formatDate(fechaMaxima, "%Y-%m-%d") + ")"
        errores.append(mensaje)

return errores