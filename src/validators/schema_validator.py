"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Validador de esquema de datos
AUTOR:       Fisherk2
FECHA:       2026-02-12
DESCRIPCIÓN: Validador de estructura del esquema de validación.
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""

from typing import List, Dict, Any

class SchemaValidator:
    """
    Componente responsable de validar la estructura del esquema de validación
    """

    # ⋮⋮⋮⋮⋮⋮⋮⋮ Definir la estructura del esquema como tipo ⋮⋮⋮⋮⋮⋮⋮⋮
    SchemaDefinition = Dict[str, Dict]

    def validate_schema_structure(self, schema: SchemaDefinition) -> bool:
        """
        Valida que el esquema tenga la estructura correcta
        :param schema: Diccionario que define el esquema de validación
        :return: ¿El Esquema es válido?
        """
        if schema is None:
            return False

        for field_name, field_def in schema.items():
            if not self._is_valid_field_definition(field_def):
                return False

        return True

    def _is_valid_field_definition(self, field_def: Dict) -> bool:
        """
        Valida la definicion de un campo individual en el esquema
        :param field_def: Diccionario con la definicion de un campo
        :return: ¿La definicion es valida?
        """
        if field_def is None:
            return False

        # ■■■■■■■■■■■■■ Verificar que exista la clave 'tipo' ■■■■■■■■■■■■■
        if "tipo" not in field_def:
            return False

        # ■■■■■■■■■■■■■ Verificar que 'tipo' sea una cadena ■■■■■■■■■■■■■
        field_type = field_def["tipo"]
        if not isinstance(field_type, str):
            return False

        # TODO: ■■■■■■■■■■■■■ Verificar que el tipo sea uno de los tipos soportados ■■■■■■■■■■■■■
        supported_types = ["entero","flotante","cadena","booleano"]
        if not field_type.lower() in supported_types:
            return False

        # ■■■■■■■■■■■■■ Verificar que 'requerido' exista y sea booleano si está presente ■■■■■■■■■■■■■
        if "requerido" in field_def:
            required_value = field_def["requerido"]
            if not isinstance(required_value, bool):
                return False

        return True

    def get_required_fields(self, schema: SchemaDefinition) -> List[str]:
        """
        Extrae la lista de campos requeridos del esquema
        :param schema: Diccionario que defina el esquema de validacion
        :return: Lista de nombres de campos que son requeridos
        """
        required_fields = List()
        if schema is None:
            return required_fields

        for field_name, field_def in schema.items():
            if self._is_valid_field_definition(field_def):
                is_required = field_def.get("requerido", False)

                # ■■■■■■■■■■■■■ Extrae el campo requerido ■■■■■■■■■■■■■
                if is_required:
                    required_fields.append(field_name)
        return required_fields

# ▼△▼△▼△▼△▼△▼△▼△▼△▼△ Pseudocodigo △▼△▼△▼△▼△▼△▼△▼△▼△▼

public List < String > getAllFieldNames(Dict < String, Dict > schema)
"""
Extrae la lista de todos los nombres de campos del esquema
Parámetros:
- schema: diccionario que define el esquema de validación
Retorna: lista de todos los nombres de campos
"""
var
fieldNames = list()

if schema != null
    fieldNames = list(schema.keys())

return fieldNames

public
boolean
fieldExistsInSchema(String
fieldName, Dict < String, Dict > schema)
"""
Verifica si un campo existe en el esquema
Parámetros:
- fieldName: nombre del campo a buscar
- schema: diccionario que define el esquema de validación
Retorna: true si el campo existe en el esquema, false en caso contrario
"""
if schema == null | | fieldName == null
    return false

return fieldName in schema