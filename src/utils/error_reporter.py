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

    def generateFieldError(self, rowNum: int, fieldName: str, errorType: str, details: str) -> List[str]:
        """
        Genera un mensaje de error para un campo específico
        :param rowNum: numero de fila donde ocurrio el error
        :param fieldName: nombre del campo con error
        :param errorType: tipo de error (tipo_incorrecto, valor_nulo, etc.)
        :param details: detalles adicionales sobre el error
        :return: Array de strings con los mensajes de error
        """
        errors = list()

        # TODO: ▼△▼△▼△▼△▼△▼△▼△▼△▼△ Refactorizar △▼△▼△▼△▼△▼△▼△▼△▼△▼
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

    def generateHeaderError(self, missingHeaders: List[str], unexpectedHeaders: List[str]) -> List[str]:
        """
        Genera mensajes de error para problemas con encabezados
        :param unexpectedHeaders: Encabezados defectuosos
        :return: Array de strings con los mensajes de error
        """
        errors = list()

        for header in missingHeaders:
            errors.extend(self.generateFieldError(
                rowNum=0,
                fieldName=header,
                errorType="campo_faltante",
                details="")
            )

        for header in unexpectedHeaders:
            errorMsg = f"Archivo: Campo no esperado '{header}' encontrado en encabezados"
            errors.append(errorMsg)
        return errors

    def generateFileError(self, fileName: str, errorType: str, details: str) -> List[str]:
        """
        Genera mensajes de error relacionados con el archivo en sí
        :param fileName: Nombre del fichero
        :param errorType: Error lanzando
        :param details: Especificación del error
        :return: Array de strings con los mensajes de error
        """
        errors = list()

        # TODO: ▼△▼△▼△▼△▼△▼△▼△▼△▼△ Refactorizar △▼△▼△▼△▼△▼△▼△▼△▼△▼
        if errorType == "archivo_no_existe":
            errorMsg = f"Archivo: '{fileName}' no existe"
            errors.append(errorMsg)
        elif errorType == "formato_invalido":
            errorMsg = f"Archivo: No se pudo leer '{fileName}' - {details}"
            errors.append(errorMsg)
        elif errorType == "lectura_fallida":
            errorMsg = f"Archivo: No se pudo leer '{fileName}' - {details}"
            errors.append(errorMsg)
        else:
            errorMsg = f"Archivo: error en '{fileName}' - {details}"
            errors.append(errorMsg)
        return errors