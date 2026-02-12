"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Error Reporter
AUTOR:       Fisherk2
FECHA:       2026-02-11
DESCRIPCIÓN: Generador de mensajes de error consistentes para el validador de CSV
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""
import os
from typing import List, Dict, Any

class ErrorReporter:
    """
    Generador de mensajes de error consistentes para el validador CSV
    """

def generateFIeldError(rowNum: int, fieldName: str, errorType: str, details: str) -> List[str]:
    """
    Genera un mensaje de error para un campo específico
    :param rowNum: numero de fila donde ocurrio el error
    :param fieldName: nombre del campo con error
    :param errorType: tipo de error (tipo_incorrecto, valor_nulo, etc.)
    :param details: detalles adicionales sobre el error
    :return: Array de strings con los mensajes de error
    """
    errors = list()

    if errorType == "tipo_incorrecto":
        errorMsg = f"Fila {rowNum}: valor no {details} en columna '{fieldName}'"
        errors.append(errorMsg)
    elif errorType == "valor_nulo":
        errorMsg = f"Fila {rowNum}: campo requerido '{fieldName}' está vacío"
        errors.append(errorMsg)
    elif errorType == "campo_faltante":
        errorMsg = f"Archivo: campo requerido '{fieldName}' no encontrado en encabezados"
        errors.append(errorMsg)
    elif errorType == "campo_no_permitido":
        errorMsg = f"Fila {rowNum}: campo '{fieldName}' no permitido según esquema"
        errors.append(errorMsg)
    else:
        errorMsg = f"Fila {rowNum}: error en campo '{fieldName}' - {details}"
        errors.append(errorMsg)

    return errors

# ▏▎▍▌▋▊▉▉▉▉▉▉▉▉ Pseudocódigo ▉▉▉▉▉▉▉▉▉▊▋▌▍▎▏

public List < String > generateHeaderError(List < String > missingHeaders, List < String > unexpectedHeaders)
"""
Genera mensajes de error para problemas con encabezados
"""
var
errors = list()

for header in missingHeaders
    errors.extend(this.generateFieldError(0, header, "campo_faltante", ""))

for header in unexpectedHeaders
    var
    errorMsg = "archivo: campo no esperado '" + header + "' encontrado en encabezados"
    errors.append(errorMsg)

return errors

public
List < String > generateFileError(String
fileName, String
errorType, String
details)
"""
Genera mensajes de error relacionados con el archivo en sí
"""
var
errors = list()

if errorType == "archivo_no_existe"
    var
    errorMsg = "archivo: '" + fileName + "' no existe"
    errors.append(errorMsg)
else if errorType == "formato_invalido"
var
errorMsg = "archivo: '" + fileName + "' no es un archivo CSV válido"
errors.append(errorMsg)
else if errorType == "lectura_fallida"
    var
    errorMsg = "archivo: no se pudo leer '" + fileName + "' - " + details
    errors.append(errorMsg)
else
    var
    errorMsg = "archivo: error en '" + fileName + "' - " + details
    errors.append(errorMsg)

return errors
