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

    # ▼△▼△▼△▼△▼△▼△▼△▼△▼△ Pseudocodigo △▼△▼△▼△▼△▼△▼△▼△▼△▼


private Lis t <Strin g> validateHeaders(Lis t <Strin g> fileHeaders, Dic t <String, Dic t> schema)
"""
Valida que los encabezados del archivo coincidan con el esquema
"""
var errors = list()

# Obtener campos requeridos del esquema
var requiredFields = this.schemaValidator.getRequiredFields(schema)

# Verificar campos faltantes
var missingHeaders = list()
for field in requiredFields
    if !field in fileHeaders
    missingHeaders.append(field)

# Verificar campos no permitidos
var allowedFields = this.schemaValidator.getAllFieldNames(schema)
var unexpectedHeaders = list()
for header in fileHeaders
    if !header in allowedFields
    unexpectedHeaders.append(header)

# Generar errores si hay discrepancias
if missingHeaders.size() > 0 || unexpectedHeaders.size() > 0
    var
    headerErrors = this.errorReporter.generateHeaderError(missingHeaders, unexpectedHeaders)
    errors.extend(headerErrors)

return errors

private
boolean
hasCriticalHeaderErrors(List < String > headerErrors)
"""
Determina si hay errores de encabezado críticos que impidan continuar
"""
for error in headerErrors
    if "campo requerido" in error | | "no encontrado" in error
        return true
return false

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