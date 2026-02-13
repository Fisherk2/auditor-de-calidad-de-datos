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
        # ■■■■■■■■■■■■■ Convertir tipo string a tipo real para validación ■■■■■■■■■■■■■
        lower_type = expected_type.lower()

        # ■■■■■■■■■■■■■ Valores nulos/vacíos se consideran válidos para validación de tipo ■■■■■■■■■■■■■
        if value == None or value == "":
            # ■■■■■■■■■■■■■ La validación de nulos se hace por separado ■■■■■■■■■■■■■
            return True

        # ■■■■■■■■■■■■■ Eliminar espacios en blanco iniciales y finales ■■■■■■■■■■■■■
        value = str(value).strip()

        # TODO: ■■■■■■■■■■■■■ Refactorizar ■■■■■■■■■■■■■
        if lower_type == "entero":
            return self._is_valid_integer(value)
        elif lower_type == "flotante":
            return self._is_valid_float(value)

        # ■■■■■■■■■■■■■ Cualquier valor se puede representar como cadena ■■■■■■■■■■■■■
        elif lower_type == "cadena":
            return True

        elif lower_type == "booleano":
            return self._is_valid_bool(value)

        # ■■■■■■■■■■■■■ Tipo desconocido ■■■■■■■■■■■■■
        else:
            return False

    def convert_value(self, value: Any, expected_type:str) -> Any:
        """
        Convierte un valor al tipo esperado de forma segura
        :param value: Valor a convertir
        :param expected_type: Tipo al que se debe convertir
        :return: Valor convertido o null si no se puede convertir
        """
        if value == None or value == "":
            return None

        # ■■■■■■■■■■■■■ Formatear valor para procesarlo ■■■■■■■■■■■■■
        value = str(value).strip()
        lowerType = expected_type.lower()

        try:

            # TODO: ■■■■■■■■■■■■■ Refactorizar ■■■■■■■■■■■■■
            if lowerType == "entero":
                return int(value)
            elif lowerType == "flotante":
                return float(value)
            elif lowerType == "cadena":
                return value
            elif lowerType == "booleano":
                return self.parse_bool(value)

            # ■■■■■■■■■■■■■ Tipo desconocido ■■■■■■■■■■■■■
            else:
                return None

        except(ValueError):

            # ■■■■■■■■■■■■■ Error en la conversion ■■■■■■■■■■■■■
            return None

        except(TypeError):

            # ■■■■■■■■■■■■■ Error en la conversion ■■■■■■■■■■■■■
            return None


    # ▣▢▣▢▣▢▣▢▣▢▣▢▣▢▣▢▣▢▣▢▣▢▣▢▣  Validadores especificos ▣▢▣▢▣▢▣▢▣▢▣▢▣▢▣▢▣▢▣▢▣▢▣▢▣

    def _is_valid_integer(self, value: str) -> bool:
        """
        Verifica si un string representa un valor entero válido
        :param value: Valor que quieres validar
        :return: ¿Es un entero?
        """
        if value is None or value.strip() == "":
            return False
        
        try:
            int(value.strip())
            return True
        except ValueError:
            return False

    def _is_valid_float(self, value: str) -> bool:
        """
        Verifica si un string representa un valor flotante válido
        :param value: Valor que quieres validar
        :return: ¿Es un flotante?
        """
        if value is None or value.strip() == "":
            return False

        try:
            float(value.strip())
            return True
        except ValueError:
            return False

    def _is_valid_bool(self, value: str) -> bool:
        """
        Verifica si un string representa un valor booleano válido
        Acepta: "true", "false", "1", "0", "si", "no", "verdadero", "falso"
        :param value: Valor que quieres validar
        :return: ¿Es un booleano?
        """
        if value is None:
            return False

        lowerValue = value.strip().lower()

        # TODO: ■■■■■■■■■■■■■ Refactorizar ■■■■■■■■■■■■■
        return lowerValue in ["true", "false", "1", "0", "si", "no", "verdadero", "falso", "t", "f"]



# ▼△▼△▼△▼△▼△▼△▼△▼△▼△ Pseudocodigo △▼△▼△▼△▼△▼△▼△▼△▼△▼

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
