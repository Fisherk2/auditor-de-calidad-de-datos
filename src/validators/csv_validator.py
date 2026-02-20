"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Validador de archivos CSV
AUTOR:       Fisherk2
FECHA:       2026-02-13
DESCRIPCIÓN: Coordinador de validacion completa de archivos CSV
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""
from typing import Any

from src.readers.csv_reader import CSVReader
from src.validators.type_validator import TypeValidator
from src.validators.schema_validator import SchemaValidator
from src.utils.csv_error_reporter import CSVErrorReporter


class CSVValidator:
    """
    Componente principal que coordina la validacion completa de archivos CSV
    """

    # ⋮⋮⋮⋮⋮⋮⋮⋮ Definir la estructura del esquema como tipo ⋮⋮⋮⋮⋮⋮⋮⋮
    SchemaDefinition = dict[str, dict]

    def __init__(self):
        self.csv_reader = CSVReader()
        self.type_validator = TypeValidator()
        self.schema_validator = SchemaValidator()
        self.error_reporter = CSVErrorReporter()

    def validate_file(self, filepath: str, schema: SchemaDefinition) -> list[str]:
        """
        Valida un archivo CSV completo contra un esquema
        :param filepath: Ruta del archivo CSV a validar
        :param schema: Esquema de validacion que define tipos y campos requeridos
        :return: Lista de mensajes de error encontrados
        """
        all_errors = list()

        # ■■■■■■■■■■■■■ Validar estructura del esquema ■■■■■■■■■■■■■
        if not self.schema_validator.validate_schema_structure(schema):
            schema_error = self.error_reporter.generate_file_error(
                file_name=filepath,
                error_type="esquema_invalido",
                details="El esquema de validacion no tiene la estructura correcta"
            )
            all_errors.extend(schema_error)
            return all_errors

        # ■■■■■■■■■■■■■ Verificar existencia del archivo ■■■■■■■■■■■■■
        if not self.csv_reader.validate_file_exist(filepath):
            file_error = self.error_reporter.generate_file_error(
                file_name=filepath,
                error_type="archivo_no_existe",
                details=""
            )
            all_errors.extend(file_error)
            return all_errors

        # ■■■■■■■■■■■■■ Validar contenido del fichero ■■■■■■■■■■■■■
        try:

            # ▲▲▲▲▲▲ Leer encabezados del archivo ▲▲▲▲▲▲
            file_headers = self.csv_reader.read_headers(filepath)

            # ▲▲▲▲▲▲ Validar encabezados contra esquema ▲▲▲▲▲▲
            headers_errors = self._validate_headers(
                file_headers=file_headers,
                schema=schema
            )
            all_errors.extend(headers_errors)

            # ▲▲▲▲▲▲ Si hay errores en los encabezados, no continuar con la validacion de filas ▲▲▲▲▲▲
            if self._has_critical_headers_errors(headers_errors):
                return all_errors

            # ▲▲▲▲▲▲ Validar cada fila del archivo ▲▲▲▲▲▲
            row_index = 1  # Empezar en 1 porque la fila 0 son encabezados
            for row in self.csv_reader.read_rows(filepath):
                row_index += 1
                row_errors = self._validate_row(
                    row=row,
                    schema=schema,
                    row_num=row_index
                )
                all_errors.extend(row_errors)

        except IOError:
            file_error = self.error_reporter.generate_file_error(
                file_name=filepath,
                error_type="lectura_fallida",
                details="No se pudo leer el fichero CSV"
            )
            all_errors.extend(file_error)
        except ValueError:
            file_error = self.error_reporter.generate_file_error(
                file_name=filepath,
                error_type="formato_invalido",
                details="Formato invalido para archivos CSV"
            )
            all_errors.extend(file_error)

        return all_errors

    def _validate_headers(self, file_headers: list[str], schema: SchemaDefinition) -> list[str]:
        """
        Valida que los encabezados del archivo coincidan con el esquema
        :param file_headers: Lista de encabezados del archivo CSV
        :param schema: Esquema de validacion que define tipos y campos requeridos
        :return: Lista de errores en encabezados.
        """
        errors = list()

        # ■■■■■■■■■■■■■ Obtener campos requeridos del esquema ■■■■■■■■■■■■■
        required_fields = self.schema_validator.get_required_fields(schema)

        # ■■■■■■■■■■■■■ Verificar campos faltantes ■■■■■■■■■■■■■
        missing_headers = list()
        for field in required_fields:
            if not field in file_headers:
                missing_headers.append(field)

        # ■■■■■■■■■■■■■ Verificar campos no permitidos ■■■■■■■■■■■■■
        allowed_fields = self.schema_validator.get_all_field_names(schema)
        unexpected_headers = list()
        for header in file_headers:
            if not header in allowed_fields:
                unexpected_headers.append(header)

        # ■■■■■■■■■■■■■ Generar errores si hay discrepancias ■■■■■■■■■■■■■
        if len(missing_headers) > 0 or len(unexpected_headers) > 0:
            header_errors = self.error_reporter.generate_header_error(
                missing_headers=missing_headers,
                unexpected_headers=unexpected_headers
            )
            errors.extend(header_errors)

        return errors

    def _has_critical_headers_errors(self, headers_errors: list[str]) -> bool:
        """
        Determina si hay errores de encabezado criticos que impidan continuar
        :param headers_errors: Lista de encabezados con posibles errores
        :return: ¿Hay errores criticos en los encabezados?
        """
        for error in headers_errors:
            if "campo requerido" in error or "no encontrado" in error:
                return True
        return False

    def _validate_row(self, row: dict[str, str], schema: SchemaDefinition, row_num: int) -> list[str]:
        """
        Valida una fila individual contra el esquema
        :param row: Fila completa del archivo CSV
        :param schema: Esquema de validacion que define tipos y campos requeridos
        :param row_num: Numero de fila del archivo CSV
        :return: Lista de errores encontrado en la fila del archivo CSV
        """
        errors = list()

        # ■■■■■■■■■■■■■ Validar cada campo en la fila ■■■■■■■■■■■■■
        for field_name, field_value in row.items():

            # ▲▲▲▲▲▲ Verificar si el campo esta permitido en el esquema ▲▲▲▲▲▲
            if self.schema_validator.field_exist_in_schema(field_name=field_name, schema=schema):
                field_schema = schema[field_name]
                field_errors = self._validate_field(field_name, field_value, field_schema, row_num)
                errors.extend(field_errors)

            # ▲▲▲▲▲▲ Campo no permitido en el esquema ▲▲▲▲▲▲
            else:
                field_errors = self.error_reporter.generate_field_error(
                    row_num=row_num,
                    field_name=field_name,
                    error_type="campo_no_permitido",
                    details=""
                )
                errors.extend(field_errors)

        # ■■■■■■■■■■■■■ Validar campos requeridos que podrian estar ausentes ■■■■■■■■■■■■■
        all_field_names = self.schema_validator.get_all_field_names(schema)
        for field_name in all_field_names:
            field_schema = schema[field_name]
            is_required = field_schema.get("requerido", False)
            if is_required and not (field_name in row):
                field_errors = self.error_reporter.generate_field_error(
                    row_num=row_num,
                    field_name=field_name,
                    error_type="valor_nulo",
                    details=""
                )
                errors.extend(field_errors)

        return errors

    def _validate_field(self, field_name: str, field_value: Any, field_schema: dict, row_num: int) -> list[str]:
        """
        Valida un campo individual segun su definicion en el esquema
        :param field_name: Nombre del campo
        :param field_value: Valor a evaluar de dicho campo
        :param field_schema: Campo del esquema de referencia para evaluar
        :param row_num: Numero de fila del archivo CSV
        :return: Lista de errores encontrado en el campo.
        """
        errors = list()

        # ■■■■■■■■■■■■■ Verificar si es un campo requerido y esta vacio ■■■■■■■■■■■■■
        is_required = field_schema.get("requerido", False)
        if is_required and ((field_value is None) or str(field_value).strip() == ""):
            field_errors = self.error_reporter.generate_field_error(
                row_num=row_num,
                field_name=field_name,
                error_type="valor_nulo",
                details=""
            )
            errors.extend(field_errors)

        # ■■■■■■■■■■■■■ Validar tipo de dato ■■■■■■■■■■■■■
        expected_type = field_schema.get("tipo", "cadena")
        if field_value is not None and str(field_value).strip() != "":
            is_valid_type = self.type_validator.validate_type(
                value=field_value,
                expected_type=expected_type
            )
            if not is_valid_type:
                type_error_details = f"{expected_type} no valido"
                field_errors = self.error_reporter.generate_field_error(
                    row_num=row_num,
                    field_name=field_name,
                    error_type="tipo_incorrecto",
                    details=type_error_details
                )
                errors.extend(field_errors)

        return errors
