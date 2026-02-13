"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Validador de archivos CSV
AUTOR:       Fisherk2
FECHA:       2026-02-12
DESCRIPCIÓN: Coordinador de validacion completa de archivos CSV
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""

import os
import csv
from typing import List, Dict, Any, Iterator

from sqlalchemy import true, false

from src.readers.csv_reader import CSVReader
from src.validators.type_validator import TypeValidator
from src.validators.schema_validator import SchemaValidator
from src.utils.error_reporter import ErrorReporter

class CSVValidator:
    """
    Componente principal que coordina la validacion completa de archivos CSV
    """

    # ⋮⋮⋮⋮⋮⋮⋮⋮ Definir la estructura del esquema como tipo ⋮⋮⋮⋮⋮⋮⋮⋮
    SchemaDefinition = Dict[str, Dict]

    def __init__(self):
        self.csv_reader = CSVReader()
        self.type_validator = TypeValidator()
        self.schema_validator = SchemaValidator()
        self.error_reporter = ErrorReporter()

    def validate_file(self,filepath:str,schema:SchemaDefinition) -> List[str]:
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
        if self.csv_reader.validate_file_exist(filepath):
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
            headers_errors = self._validate_headers(file_headers, schema)
            all_errors.extend(headers_errors)

            # ▲▲▲▲▲▲ Si hay errores en los encabezados, no continuar con la validacion de filas ▲▲▲▲▲▲
            if self._has_critical_headers_errors(headers_errors):
                return all_errors

            # ▲▲▲▲▲▲ Validar cada fila del archivo ▲▲▲▲▲▲
            row_index = 1 # Empezar en 1 porque la fila 0 son encabezados
            for row in self.csv_reader.read_rows(filepath):
                row_index += 1
                row_errors = self._validate_row(filepath)
                all_errors.extend(row_errors)

        except(IOError):
            file_error = self.error_reporter.generate_file_error(
                file_name=filepath,
                error_type="lectura_fallida",
                details="No se pudo leer el fichero CSV"
            )
            all_errors.extend(file_error)
        except(ValueError):
            file_error = self.error_reporter.generate_file_error(
                file_name=filepath,
                error_type="formato_invalido",
                details="Formato invalido para archivos CSV"
            )
            all_errors.extend(file_error)

        return all_errors

    def _validate_headers(self, file_headers: List[str], schema:SchemaDefinition) -> List[str]:
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
        if missing_headers.size() > 0 or unexpected_headers.size() > 0:
            header_errors = self.error_reporter.generate_header_error(
                missing_headers=missing_headers,
                unexpected_headers=unexpected_headers
            )
            errors.extend(header_errors)

        return errors

    def _has_critical_header_errors(self, headers_errors:List[str]) -> bool:
        """
        Determina si hay errores de encabezado criticos que impidan continuar
        :param headers_errors: Lista de encabezados con posibles errores
        :return: ¿Hay errores criticos en los encabezados?
        """
        for error in headers_errors:
            if "campo requerido" in error or "no encontrado" in error:
                return True
        return False

    # ▼△▼△▼△▼△▼△▼△▼△▼△▼△ Pseudocodigo △▼△▼△▼△▼△▼△▼△▼△▼△▼

private
List < String > validateRow(Dict < String, String > row, Dict < String, Dict > schema, int
rowNum)
"""
Valida una fila individual contra el esquema
"""
var
errors = list()

# Validar cada campo en la fila
for fieldName, fieldValue in row.items()
    # Verificar si el campo está permitido en el esquema
    if this.schemaValidator.fieldExistsInSchema(fieldName, schema)
        var
        fieldSchema = schema[fieldName]
        var
        fieldErrors = this.validateField(fieldName, fieldValue, fieldSchema, rowNum)
        errors.extend(fieldErrors)
    else
        # Campo no permitido en el esquema
        var
        fieldErrors = this.errorReporter.generateFieldError(rowNum, fieldName, "campo_no_permitido", "")
        errors.extend(fieldErrors)

# Validar campos requeridos que podrían estar ausentes
var
allFieldNames = this.schemaValidator.getAllFieldNames(schema)
for fieldName in allFieldNames
    var
    fieldSchema = schema[fieldName]
    var
    isRequired = fieldSchema.get("requerido", false)

    if isRequired & & !(fieldName in row)
    var
    fieldErrors = this.errorReporter.generateFieldError(rowNum, fieldName, "valor_nulo", "")
    errors.extend(fieldErrors)

return errors

private
List < String > validateField(String
fieldName, Object
fieldValue, Dict
fieldSchema, int
rowNum)
"""
Valida un campo individual según su definición en el esquema
"""
var
errors = list()

# Verificar si es un campo requerido y está vacío
var
isRequired = fieldSchema.get("requerido", false)
if isRequired & & (fieldValue == null | | str(fieldValue).strip() == "")
    var
    fieldErrors = this.errorReporter.generateFieldError(rowNum, fieldName, "valor_nulo", "")
    errors.extend(fieldErrors)

# Validar tipo de dato
var
expectedType = fieldSchema.get("tipo", "cadena")
if fieldValue != null & & str(fieldValue).strip() != ""
    var
    isValidType = this.typeValidator.validateType(fieldValue, expectedType)
    if !isValidType
    var
    typeErrorDetails = "no " + expectedType + " válido"
    var
    fieldErrors = this.errorReporter.generateFieldError(rowNum, fieldName, "tipo_incorrecto", typeErrorDetails)
    errors.extend(fieldErrors)

return errors