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

        pass

# ▼△▼△▼△▼△▼△▼△▼△▼△▼△ Pseudocodigo △▼△▼△▼△▼△▼△▼△▼△▼△▼

private
boolean
isValidFieldDefinition(Dict
fieldDef)
"""
Valida la definición de un campo individual en el esquema
Parámetros:
- fieldDef: diccionario con la definición de un campo
Retorna: true si la definición es válida, false en caso contrario
"""
if fieldDef == null
    return false

# Verificar que exista la clave 'tipo'
if !"tipo" in fieldDef
return false

# Verificar que 'tipo' sea una cadena
var
fieldType = fieldDef["tipo"]
if !isinstance(fieldType, str)
return false

# Verificar que el tipo sea uno de los tipos soportados
var
supportedTypes = ["entero", "flotante", "cadena", "booleano"]
if !fieldType.lower() in supportedTypes
return false

# Verificar que 'requerido' exista y sea booleano si está presente
if "requerido" in fieldDef
    var
    requiredValue = fieldDef["requerido"]
    if !isinstance(requiredValue, bool)
    return false

return true

public
List < String > getRequiredFields(Dict < String, Dict > schema)
"""
Extrae la lista de campos requeridos del esquema
Parámetros:
- schema: diccionario que define el esquema de validación
Retorna: lista de nombres de campos que son requeridos
"""
var
requiredFields = list()

if schema == null
    return requiredFields

for fieldName, fieldDef in schema.items()
    if this.isValidFieldDefinition(fieldDef)
        var
        isRequired = fieldDef.get("requerido", false)
        if isRequired
            requiredFields.append(fieldName)

return requiredFields

public
List < String > getAllFieldNames(Dict < String, Dict > schema)
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