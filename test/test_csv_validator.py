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
        self.test_validate_non_existent_file()
        self.test_validate_unexpected_headers()
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
            print(f"  Errors: {str(errors)}")

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
            # TODO: ▲▲▲▲▲▲ Refactorizar ▲▲▲▲▲▲
            if "apellido" in error and "no encontrado" in error:
                has_missing_field_error = True
                break
        if has_missing_field_error:
            print("✓ testValidateMissingHeaders: PASSED")
        else:
            print("✗ testValidateMissingHeaders: FAILED - Expected missing field error")
            print(f"  Errors: {str(errors)}")

        # ■■■■■■■■■■■■■ Limpiar archivo temporal ■■■■■■■■■■■■■
        os.remove(temp_file)

    def test_validate_wrong_types(self):
        """
        Test: Validar un CSV con tipos de datos incorrectos
        :return:
        """
        # ■■■■■■■■■■■■■ Esquema de prueba ■■■■■■■■■■■■■
        schema = dict()
        schema["id"] = {"tipo": "entero", "requerido": True}
        schema["nombre"] = {"tipo": "cadena", "requerido": True}
        schema["edad"] = {"tipo": "entero", "requerido": False}

        # ■■■■■■■■■■■■■ Crear archivo temporal con tipo incorrecto ■■■■■■■■■■■■■
        temp_content = "id,nombre,edad\n1,Alice,treinta\n2,Bob,25"
        temp_file = self._create_temp_file(temp_content)
        errors = self.validator.validate_file(
            filepath=temp_file,
            schema=schema
        )

        # ■■■■■■■■■■■■■ Deberia haber error por tipo incorrecto ■■■■■■■■■■■■■
        has_type_error = False
        for error in errors:
            # TODO: ▲▲▲▲▲▲ Refactorizar ▲▲▲▲▲▲
            if "no entero valido" in error and "fila 1" in error:
                has_type_error = True
                break
        if has_type_error:
            print("✓ testValidateWrongTypes: PASSED")
        else:
            print("✗ testValidateWrongTypes: FAILED - Expected type error")
            print(f"  Errors: {str(errors)}")

        # ■■■■■■■■■■■■■ Limpiar archivo temporal ■■■■■■■■■■■■■
        os.remove(temp_file)

    def test_validate_null_values(self):
        """
        Test: Validar un CSV con valores nulos en campos requeridos
        :return:
        """
        # ■■■■■■■■■■■■■ Esquema de prueba ■■■■■■■■■■■■■
        schema = dict()
        schema["id"] = {"tipo": "entero", "requerido": True}
        schema["nombre"] = {"tipo": "cadena", "requerido": True}

        # ■■■■■■■■■■■■■ Crear archivo temporal con campo requerido vacio ■■■■■■■■■■■■■
        temp_content = "id,nombre\n1,\n2,Bob"
        temp_file = self._create_temp_file(temp_content)
        errors = self.validator.validate_file(
            filepath=temp_file,
            schema=schema
        )

        # ■■■■■■■■■■■■■ Deberia haber error por valor nulo en campo requerido ■■■■■■■■■■■■■
        has_null_error = False
        for error in errors:
            # TODO: ▲▲▲▲▲▲ Refactorizar ▲▲▲▲▲▲
            if "campo requerido" in error and "está vacío" in error and "fila 1" in error:
                has_null_error = True
                break
        if has_null_error:
            print("✓ testValidateNullValues: PASSED")
        else:
            print("✗ testValidateNullValues: FAILED - Expected null value error")
            print(f"  Errors: {str(errors)}")

        # ■■■■■■■■■■■■■ Limpiar archivo temporal ■■■■■■■■■■■■■
        os.remove(temp_file)

    def test_validate_non_existent_file(self):
        """
        Test: Validar un archivo que no existe
        :return:
        """
        # ■■■■■■■■■■■■■ Esquema de prueba ■■■■■■■■■■■■■
        schema = dict()
        schema["id"] = {"tipo": "entero", "requerido": True}

        # ■■■■■■■■■■■■■ Declarar un directorio que no existe ■■■■■■■■■■■■■
        non_existent_file = "/path/that/does/not/exist.csv"
        errors = self.validator.validate_file(
            filepath=non_existent_file,
            schema=schema
        )

        # ■■■■■■■■■■■■■ Deberia haber error de archivo no existente ■■■■■■■■■■■■■
        has_file_error = False
        for error in errors:
            # TODO: ▲▲▲▲▲▲ Refactorizar ▲▲▲▲▲▲
            if "no existe" in error:
                has_file_error = True
                break
        if has_file_error:
            print("✓ testValidateNonExistentFile: PASSED")
        else:
            print("✗ testValidateNonExistentFile: FAILED - Expected file not found error")
            print(f"  Errors: {str(errors)}")

    def test_validate_unexpected_headers(self):
        """
        Test: Validar un CSV con campos no permitidos por el esquema
        :return:
        """
        # ■■■■■■■■■■■■■ Esquema de prueba ■■■■■■■■■■■■■
        schema = dict()
        schema["id"] = {"tipo": "entero", "requerido": True}
        schema["nombre"] = {"tipo": "cadena", "requerido": True}

        # ■■■■■■■■■■■■■ Crear archivo temporal con campo no permitido ■■■■■■■■■■■■■
        temp_content = "id,nombre,apellido\n1,Alice,Pérez"
        temp_file = self._create_temp_file(temp_content)
        errors = self.validator.validate_file(
            filepath=temp_file,
            schema=schema
        )

        # ■■■■■■■■■■■■■ Deberia haber error por campo no permitido ■■■■■■■■■■■■■
        has_unexpected_field_error = False
        for error in errors:
            if "apellido" in error and "no esperado" in error:
                has_unexpected_field_error = True
                break
        if has_unexpected_field_error:
            print("✓ testValidateUnexpectedHeaders: PASSED")
        else:
            print("✗ testValidateUnexpectedHeaders: FAILED - Expected unexpected field error")
            print(f"  Errors: {str(errors)}")

        # ■■■■■■■■■■■■■ Limpiar archivo temporal ■■■■■■■■■■■■■
        os.remove(temp_file)

    def _create_temp_file(self, content:str) -> str:
        """
        Crea un archivo temporal seguro con contenido especifico
        :return:
        """
        temp_file_handle = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        temp_file_handle.write(content)

        # ■■■■■■■■■■■■■ Asegurar que el contenido se escribe ■■■■■■■■■■■■■
        temp_file_handle.flush()

        temp_file_path = temp_file_handle.name
        temp_file_handle.close()

        return temp_file_path

# ▼△▼△▼△▼△▼△▼△▼△▼△▼△ Pseudocodigo △▼△▼△▼△▼△▼△▼△▼△▼△▼

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
