"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Error Reporter
AUTOR:       Fisherk2
FECHA:       2026-02-11
DESCRIPCIÓN: Generador de mensajes de error consistentes para el validador de CSV
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""

class CSVErrorReporter:
    """
    Generador de mensajes de error consistentes para el validador CSV
    """

    def generate_field_error(self, row_num: int, field_name: str, error_type: str, details: str) -> list[str]:
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
            error_msg = f"Fila {row_num}: valor {details} en columna '{field_name}'"
            errors.append(error_msg)
        elif error_type == "valor_nulo":
            error_msg = f"Fila {row_num}: campo requerido '{field_name}' está vacío"
            errors.append(error_msg)
        elif error_type == "campo_faltante":
            error_msg = f"Archivo: campo requerido '{field_name}' no encontrado en encabezados"
            errors.append(error_msg)
        elif error_type == "campo_no_permitido":
            error_msg = f"Fila {row_num}: campo '{field_name}' no permitido según esquema"
            errors.append(error_msg)
        else:
            error_msg = f"Fila {row_num}: error en campo '{field_name}' - {details}"
            errors.append(error_msg)
        return errors

    def generate_header_error(self, missing_headers: list[str], unexpected_headers: list[str]) -> list[str]:
        """
        Genera mensajes de error para problemas con encabezados
        :param missing_headers: Encabezados faltantes
        :param unexpected_headers: Encabezados defectuosos
        :return: Array de strings con los mensajes de error
        """
        errors = list()

        for header in missing_headers:
            errors.extend(self.generate_field_error(
                row_num=0,
                field_name=header,
                error_type="campo_faltante",
                details="")
            )

        for header in unexpected_headers:
            error_msg = f"Archivo: Campo no esperado '{header}' encontrado en encabezados"
            errors.append(error_msg)
        return errors

    def generate_file_error(self, file_name: str, error_type: str, details: str) -> list[str]:
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
            error_msg = f"Archivo: '{file_name}' no existe"
            errors.append(error_msg)
        elif error_type == "formato_invalido":
            error_msg = f"Archivo: No se pudo leer '{file_name}' - {details}"
            errors.append(error_msg)
        elif error_type == "lectura_fallida":
            error_msg = f"Archivo: No se pudo leer '{file_name}' - {details}"
            errors.append(error_msg)
        else:
            error_msg = f"Archivo: error en '{file_name}' - {details}"
            errors.append(error_msg)
        return errors