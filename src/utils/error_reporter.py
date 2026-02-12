"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Error Reporter
AUTOR:       Fisherk2
FECHA:       2026-02-11
DESCRIPCIÓN: Generador de mensajes de error consistentes para el validador de CSV
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""
from typing import List

class ErrorReporter:
    """
    Generador de mensajes de error consistentes para el validador CSV
    """

    def generateFieldError(self, row_num: int, field_name: str, error_type: str, details: str) -> List[str]:
        """
        Genera un mensaje de error para un campo específico
        :param row_num: numero de fila donde ocurrio el error
        :param field_name: nombre del campo con error
        :param error_type: tipo de error (tipo_incorrecto, valor_nulo, etc.)
        :param details: detalles adicionales sobre el error
        :return: Array de strings con los mensajes de error
        """
        errors = list()

        # TODO: ▼△▼△▼△▼△▼△▼△▼△▼△▼△ Refactorizar △▼△▼△▼△▼△▼△▼△▼△▼△▼
        if error_type == "tipo_incorrecto":
            errorMsg = f"Fila {row_num}: valor no {details} en columna '{field_name}'"
            errors.append(errorMsg)
        elif error_type == "valor_nulo":
            errorMsg = f"Fila {row_num}: campo requerido '{field_name}' está vacío"
            errors.append(errorMsg)
        elif error_type == "campo_faltante":
            errorMsg = f"Archivo: campo requerido '{field_name}' no encontrado en encabezados"
            errors.append(errorMsg)
        elif error_type == "campo_no_permitido":
            errorMsg = f"Fila {row_num}: campo '{field_name}' no permitido según esquema"
            errors.append(errorMsg)
        else:
            errorMsg = f"Fila {row_num}: error en campo '{field_name}' - {details}"
            errors.append(errorMsg)
        return errors

    def generateHeaderError(self, missing_headers: List[str], unexpected_headers: List[str]) -> List[str]:
        """
        Genera mensajes de error para problemas con encabezados
        :param unexpected_headers: Encabezados defectuosos
        :return: Array de strings con los mensajes de error
        """
        errors = list()

        for header in missing_headers:
            errors.extend(self.generateFieldError(
                row_num=0,
                field_name=header,
                error_type="campo_faltante",
                details="")
            )

        for header in unexpected_headers:
            errorMsg = f"Archivo: Campo no esperado '{header}' encontrado en encabezados"
            errors.append(errorMsg)
        return errors

    def generateFileError(self, file_name: str, error_type: str, details: str) -> List[str]:
        """
        Genera mensajes de error relacionados con el archivo en sí
        :param file_name: Nombre del fichero
        :param error_type: Error lanzando
        :param details: Especificación del error
        :return: Array de strings con los mensajes de error
        """
        errors = list()

        # TODO: ▼△▼△▼△▼△▼△▼△▼△▼△▼△ Refactorizar △▼△▼△▼△▼△▼△▼△▼△▼△▼
        if error_type == "archivo_no_existe":
            errorMsg = f"Archivo: '{file_name}' no existe"
            errors.append(errorMsg)
        elif error_type == "formato_invalido":
            errorMsg = f"Archivo: No se pudo leer '{file_name}' - {details}"
            errors.append(errorMsg)
        elif error_type == "lectura_fallida":
            errorMsg = f"Archivo: No se pudo leer '{file_name}' - {details}"
            errors.append(errorMsg)
        else:
            errorMsg = f"Archivo: error en '{file_name}' - {details}"
            errors.append(errorMsg)
        return errors