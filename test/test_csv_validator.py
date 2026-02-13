"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      SUT de validador de archivos CSV
AUTOR:       Fisherk2
FECHA:       2026-02-13
DESCRIPCIÓN: Campo de pruebas unitarias para la implementacion de validador CSV
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""
import os
import tempfile
from typing import List, Dict
from src.validators.csv_validator import CSVValidator
from src.validators.type_validator import TypeValidator
from src.validators.schema_validator import SchemaValidator

class TestCSVValidator:
    """
    Suite de pruebas unitarias para el validador de CSV
    """

    def __init__(self):
        self.validator = CSVValidator()

    def run_all_test(self):
        """
        Ejecuta todas las pruebas del validador
        :return:
        """
        print("🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙 Ejecutando pruebas del validador de CSV 🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙")
        self.test_validate_correct_csv()
        self.test_validate_missing_headers()
        self.test_validate_wrong_types()
        self.test_validate_null_values()
        self.test_validates_non_existent_file()
        self.test_validates_unexpected_headers()
        print("🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙 Todas las pruebas completadas 🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙")

    def test_validate_correct_csv(self):
        """
        Test: Validar un CSV que cumple completamente con un esquema de prueba
        :return:
        """
        # ■■■■■■■■■■■■■ Esquema de prueba ■■■■■■■■■■■■■
        schema = dict()
        schema["id"] = {"tipo": "entero", "requerido": True}
        schema["nombre"] = {"tipo": "cadena", "requerido": True}
        schema["activo"] = {"tipo": "booleano", "requerido": True}

        # ■■■■■■■■■■■■■ Crear archivo temporal con datos validos ■■■■■■■■■■■■■
        temp_content= "id,nombre,activo\n1,Alice,true\n2,Bob,false"
        temp_file = self._create_temp_file(temp_content)
        errors = self.validator.validate_file(
            filepath=temp_file,
            schema=schema
        )

        # ■■■■■■■■■■■■■ Deberia haber 0 errores ■■■■■■■■■■■■■
        if len(errors) == 0:
            print("✓ testValidateCorrectCSV: PASSED")
        else:
            print(f"✗ testValidateCorrectCSV: FAILED - Expected 0 errors, got {str(len(errors))}")
            print("  Errors: " + str(errors))

        # ■■■■■■■■■■■■■ Limpiar archivo temporal ■■■■■■■■■■■■■
        os.remove(temp_file)

    def test_validate_missing_headers(self):
        """
        Test: Validar un CSV con campos requeridos faltantes
        :return:
        """
        # ■■■■■■■■■■■■■ Esquema de prueba ■■■■■■■■■■■■■
        schema = dict()
        schema["id"] = {"tipo": "entero", "requerido": True}
        schema["nombre"] = {"tipo": "cadena", "requerido": True}
        schema["activo"] = {"tipo": "cadena", "requerido": True}

        # ■■■■■■■■■■■■■ Crear archivo temporal con campo requerido faltante ■■■■■■■■■■■■■
        temp_content = "id,nombre\n1,Alice"
        temp_file = self._create_temp_file(temp_content)
        errors = self.validator.validate_file(
            filepath=temp_file,
            schema=schema
        )

        # ■■■■■■■■■■■■■ Deberia haber errores por campo faltante ■■■■■■■■■■■■■
        has_missing_field_error = False
        for error in errors:
            if "apellido" in error and "no encontrado" in error:
                has_missing_field_error = True
                break
        if has_missing_field_error:
            print("✓ testValidateMissingHeaders: PASSED")
        else:
            print("✗ testValidateMissingHeaders: FAILED - Expected missing field error")
            print("  Errors: " + str(errors))

        # ■■■■■■■■■■■■■ Limpiar archivo temporal ■■■■■■■■■■■■■
        os.remove(temp_file)


# ▼△▼△▼△▼△▼△▼△▼△▼△▼△ Pseudocodigo △▼△▼△▼△▼△▼△▼△▼△▼△▼


public
void
testValidateWrongTypes()
"""
Prueba: Validar un CSV con tipos de datos incorrectos
"""
var
schema = dict()
schema["id"] = {"tipo": "entero", "requerido": true}
schema["nombre"] = {"tipo": "cadena", "requerido": true}
schema["edad"] = {"tipo": "entero", "requerido": false}

# Crear archivo temporal con tipo incorrecto
var
tempContent = "id,nombre,edad\n1,Alice,treinta\n2,Bob,25"
var
tempFile = this.createTempFile(tempContent)

var
errors = this.validator.validateFile(tempFile, schema)

# Debería haber error por tipo incorrecto
var
hasTypeError = false
for error in errors
    if "no entero válido" in error & & "fila 1" in error
        hasTypeError = true
        break

if hasTypeError
    print("✓ testValidateWrongTypes: PASSED")
else
    print("✗ testValidateWrongTypes: FAILED - Expected type error")
    print("  Errors: " + str(errors))

# Limpiar archivo temporal
os.remove(tempFile)

public
void
testValidateNullValues()
"""
Prueba: Validar un CSV con valores nulos en campos requeridos
"""
var
schema = dict()
schema["id"] = {"tipo": "entero", "requerido": true}
schema["nombre"] = {"tipo": "cadena", "requerido": true}

# Crear archivo temporal con campo requerido vacío
var
tempContent = "id,nombre\n1,\n2,Bob"
var
tempFile = this.createTempFile(tempContent)

var
errors = this.validator.validateFile(tempFile, schema)

# Debería haber error por valor nulo en campo requerido
var
hasNullError = false
for error in errors
    if "campo requerido" in error & & "está vacío" in error & & "fila 1" in error
        hasNullError = true
        break

if hasNullError
    print("✓ testValidateNullValues: PASSED")
else
    print("✗ testValidateNullValues: FAILED - Expected null value error")
    print("  Errors: " + str(errors))

# Limpiar archivo temporal
os.remove(tempFile)

public
void
testValidateNonExistentFile()
"""
Prueba: Validar un archivo que no existe
"""
var
schema = dict()
schema["id"] = {"tipo": "entero", "requerido": true}

var
nonExistentFile = "/path/that/does/not/exist.csv"
var
errors = this.validator.validateFile(nonExistentFile, schema)

# Debería haber error de archivo no existente
var
hasFileError = false
for error in errors
    if "no existe" in error
        hasFileError = true
        break

if hasFileError
    print("✓ testValidateNonExistentFile: PASSED")
else
    print("✗ testValidateNonExistentFile: FAILED - Expected file not found error")
    print("  Errors: " + str(errors))

public
void
testValidateUnexpectedHeaders()
"""
Prueba: Validar un CSV con campos no permitidos por el esquema
"""
var
schema = dict()
schema["id"] = {"tipo": "entero", "requerido": true}
schema["nombre"] = {"tipo": "cadena", "requerido": true}

# Crear archivo temporal con campo no permitido
var
tempContent = "id,nombre,apellido\n1,Alice,Pérez"
var
tempFile = this.createTempFile(tempContent)

var
errors = this.validator.validateFile(tempFile, schema)

# Debería haber error por campo no permitido
var
hasUnexpectedFieldError = false
for error in errors
    if "apellido" in error & & "no esperado" in error
        hasUnexpectedFieldError = true
        break

if hasUnexpectedFieldError
    print("✓ testValidateUnexpectedHeaders: PASSED")
else
    print("✗ testValidateUnexpectedHeaders: FAILED - Expected unexpected field error")
    print("  Errors: " + str(errors))

# Limpiar archivo temporal
os.remove(tempFile)

private
String
createTempFile(String
content)
"""
Crea un archivo temporal con contenido específico
"""
var
tempFile = tempfile.mktemp(suffix=".csv")
with open(tempFile, 'w') as file
    file.write(content)
return tempFile


# 3. MAIN EXECUTION
class Main
    public
    static
    void
    main(String[]
    args)
    var
    tester = new
    TestCSVValidator()
    tester.runAllTests()
