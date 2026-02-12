"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Validador y conversor de tipos
AUTOR:       Fisherk2
FECHA:       2026-02-12
DESCRIPCIÓN: Validador y conversor de tipos establecido en el esquema
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""
import os
from typing import List, Dict, Any, Union

class TypeValidator:
    """
    Componente responsable de validar tipos de datos y realizar conversiones seguras
    """
    def validate_type(self, value: Any, expected_type: str) -> bool:
        """
        Valida si un valor coincide con el tipo esperado
        :param value: Valor a validar
        :param expected_type: Tipo esperado ("entero", "flotante", "cadena", "booleano")
        :return: ¿Es del tipo esperado?
        """
        # ▲▲▲▲▲▲▲▲▲▲▲▲▲ Convertir tipo string a tipo real para validación ▲▲▲▲▲▲▲▲▲▲▲▲▲
        lower_type = expected_type.lower()
        if value == None or value == "":
            # ■■■■■■■■■■■■■ Valores nulos/vacíos se consideran válidos para validación de tipo ■■■■■■■■■■■■■
            # ■■■■■■■■■■■■■ La validación de nulos se hace por separado ■■■■■■■■■■■■■
            return True

        # ▲▲▲▲▲▲▲▲▲▲▲▲▲ Eliminar espacios en blanco iniciales y finales ▲▲▲▲▲▲▲▲▲▲▲▲▲
        value = str(value).strip()

        # TODO: ■■■■■■■■■■■■■ Refactorizar ■■■■■■■■■■■■■
        if lower_type == "entero":
            return self.is_valid_integer(value)
        elif lower_type == "flotante":
            return self.is_valid_float(value)

        # ■■■■■■■■■■■■■ Cualquier valor se puede representar como cadena ■■■■■■■■■■■■■
        elif lower_type == "cadena":
            return True

        elif lower_type == "booleano":
            return self.is_valid_boolean(value)

        # ■■■■■■■■■■■■■ Tipo desconocido ■■■■■■■■■■■■■
        else:
            return False


# ▼△▼△▼△▼△▼△▼△▼△▼△▼△ Pseudocodigo △▼△▼△▼△▼△▼△▼△▼△▼△▼


public Object convertValue(Object value, String expectedType)
"""
Convierte un valor al tipo esperado de forma segura
Parámetros:
- value: valor a convertir
- expectedType: tipo al que se debe convertir
Retorna: valor convertido o null si no se puede convertir
"""
if value == null | | value == ""
    return null

var
stringValue = str(value).strip()
var
lowerType = expectedType.lower()

try
    if lowerType == "entero"
        return int(stringValue)
    else if lowerType == "flotante"
    return float(stringValue)
else if lowerType == "cadena"
    return stringValue
else if lowerType == "booleano"
return this.parseBoolean(stringValue)
else
# Tipo desconocido
return null
catch
ValueError
e
# Error en la conversión
return null
catch
TypeError
e
# Error en la conversión
return null

private
boolean
isValidInteger(String
value)
"""
Verifica si un string representa un valor entero válido
"""
if value == null | | value.strip() == ""
    return false

try
    var
    intValue = int(value.strip())
    return true
catch
ValueError
e
return false

private
boolean
isValidFloat(String
value)
"""
Verifica si un string representa un valor flotante válido
"""
if value == null | | value.strip() == ""
    return false

try
    var
    floatValue = float(value.strip())
    return true
catch
ValueError
e
return false

private
boolean
isValidBoolean(String
value)
"""
Verifica si un string representa un valor booleano válido
Acepta: "true", "false", "1", "0", "si", "no", "verdadero", "falso"
"""
if value == null
    return false

var
lowerValue = value.strip().lower()
return lowerValue in ["true", "false", "1", "0", "si", "no", "verdadero", "falso", "t", "f"]

private
boolean
parseBoolean(String
value)
"""
Convierte un string a valor booleano
"""
if value == null
    return false

var
lowerValue = value.strip().lower()
return lowerValue in ["true", "1", "si", "verdadero", "t"]
