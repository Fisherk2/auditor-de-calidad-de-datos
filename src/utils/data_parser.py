"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Parseo y validación básica de datos de entrada
AUTOR:       Fisherk2
FECHA:       2026-02-16
DESCRIPCIÓN: Capa de acceso a datos que proporciona funciones para validar y transformar datos de entrada
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""

from typing import Any, List, Dict
import yaml
import csv

# ⋮⋮⋮⋮⋮⋮⋮⋮ ALIAS de estructura datos ⋮⋮⋮⋮⋮⋮⋮⋮
RowDataType = list[dict[str, Any]]
ColumnIndexMap = dict[str, list[int]]


class DataParser:
    """
    Clase de utilidad para parseo y validación de datos estructurados
    """

    @staticmethod
    def is_numeric_value(value: Any) -> bool:
        """
        Verifica si un valor puede ser convertido a número
        :param value:
        :return: ¿Es un valor numérico?
        """
        if value is None:
            return False
        if isinstance(value, (int, float)):
            return True
        if isinstance(value, str):
            try:
                float(value)
                return True
            except ValueError:
                return False
        return False

    @staticmethod
    def is_string_value(value: Any) -> bool:
        """
        Verifica si un valor es una cadena valida (no vacia)
        :param value:
        :return: ¿Es una cadena valida?
        """
        if value is None:
            return False
        if isinstance(value, str):
            return len(value.strip()) > 0
        return False

    @staticmethod
    def is_bool_value(value: Any) -> bool:
        """
        Verifica si un valor puede ser interpretado como booleano
        :param value:
        :return: ¿Es un valor booleano?
        """
        if value is None:
            return False
        if isinstance(value, bool):
            return True
        if isinstance(value, str):
            lower_value = value.lower().strip()

            # TODO: ▁▂▃▄▅▆▇███████ Interpretaciones aceptadas ███████▇▆▅▄▃▂▁
            return (
                    lower_value == "true" or lower_value == "false" or
                    lower_value == "1" or lower_value == "0" or
                    lower_value == "yes" or lower_value == "no" or
                    lower_value == "on" or lower_value == "off"
            )

        return False

    @staticmethod
    def is_null_value(value: Any) -> bool:
        """
        Verifica si un valor es nulo o representa un valor nulo
        :param value:
        :return: ¿Es un valor nulo?
        """
        if value is None:
            return True
        if isinstance(value, str):
            trimmed = value.lower().strip()

            # TODO: ▁▂▃▄▅▆▇███████ Interpretaciones aceptadas ███████▇▆▅▄▃▂▁
            return (
                    trimmed == "" or trimmed == "null" or
                    trimmed == "none" or trimmed == "na" or
                    trimmed == "n/a" or trimmed == "<null>"
            )

        return False

    @staticmethod
    def get_column_index(data: RowDataType) -> ColumnIndexMap:
        """
        Obtiene los indices de aparicion de cada columna de los datos
        para recibir una lista de diccionarios (que representan filas de datos)
        y devolver un diccionario que mapea cada nombre de columna
        a una lista de los índices (posiciones) de las filas en las que
        esa columna aparece.
        :return: Diccionario de indices de cada columna
        """
        if not data:
            return dict()

        # ■■■■■■■■■■■■■ Obtenemos la primera fila de datos para conocer las columnas existentes ■■■■■■■■■■■■■
        column_index = dict()
        first_row = data[0]

        # ■■■■■■■■■■■■■ Iteramos sobre cada clave (nombre de columna) en la primera fila ■■■■■■■■■■■■■
        for key in first_row.keys():
            indexes = list()

            # ■■■■■■■■■■■■■ Recorremos cada fila en los datos (usando su índice) ■■■■■■■■■■■■■
            for i in range(len(data)):
                if key in data[i]:
                    indexes.append(i)

            # ■■■■■■■■■■■■■ Una vez recorridas todas las filas, asignamos la lista de índices al nombre de la columna ■■■■■■■■■■■■■
            column_index[key] = indexes

        return column_index

    @staticmethod
    def validate_row_structure(row: dict[str, Any], expected_columns: set[str]) -> dict[str, Any]:
        """
        Valida la estructura de una fila contra columnas esperadas
        :return: Diccionario de resultados que validan la fila
        """
        result = dict()
        result["valid"] = True
        result["missing_columns"] = list()
        result["extra_columns"] = list()

        # ■■■■■■■■■■■■■ Verificar columnas faltantes ■■■■■■■■■■■■■
        for expected_column in expected_columns:
            if not expected_column in row.keys():
                result["missing_columns"].append(expected_column)

        # ■■■■■■■■■■■■■ Verificar columnas extra ■■■■■■■■■■■■■
        for actual_column in row.keys():
            if not actual_column in expected_columns:
                result["extra_columns"].append(actual_column)

        has_issues = result["missing_columns"] or result["extra_columns"]
        result["valid"] = not has_issues

        return result

    @staticmethod
    def filter_valid_rows(data: RowDataType, expected_columns: set[str], rules_config: Dict[str, Any] = None) -> RowDataType:
        """
        Filtra filas que contienen todas las columnas esperadas
        Opcionalmente, aplica reglas de calidad desde la configuracion
        :param data: Datos a filtrar
        :param expected_columns: Columnas esperadas
        :param rules_config: Configuración de reglas (opcional)
        :return: Filas válidas filtradas
        """
        valid_rows = list()
        for row in data:
            validation = DataParser.validate_row_structure(
                row=row,
                expected_columns=expected_columns
            )
            if validation["valid"]:

                # ■■■■■■■■■■■■■ Aplicar reglas de calidad (OPCIONAL) ■■■■■■■■■■■■■
                if rules_config:
                    if DataParser.validarContraReglas([row], rules_config):
                        valid_rows.append(row)
                else:
                    valid_rows.append(row)

        return valid_rows

    @staticmethod
    def validarContraReglas(datos: List[Dict[str, Any]], reglasConfig: Dict[str, Any]) -> bool:
        """
        Aplica reglas de validación desde configuración YAML
        :param datos: Datos a validar
        :param reglasConfig: Configuración de reglas desde YAML
        :return: True si los datos cumplen las reglas, False otherwise
        """
        if not reglasConfig or 'quality_rules' not in reglasConfig:
            return True

        quality_rules = reglasConfig['quality_rules']
        general_rules = quality_rules.get('general', {})
        data_type_rules = quality_rules.get('data_type_rules', {})

        # Validar reglas generales
        for row in datos:
            # Verificar porcentaje de nulos
            null_count = sum(1 for value in row.values() if DataParser.is_null_value(value))
            null_percentage = (null_count / len(row)) * 100 if len(row) > 0 else 0
            
            max_null_percentage = general_rules.get('max_null_percentage', 50.0)
            if null_percentage > max_null_percentage:
                return False

            # Validar tipos de datos específicos
            for column, value in row.items():
                if DataParser.is_null_value(value):
                    continue

                # Determinar tipo de dato y aplicar reglas
                if DataParser.is_numeric_value(value):
                    numeric_rules = data_type_rules.get('numeric', {})
                    if not numeric_rules.get('allow_negative', True) and float(value) < 0:
                        return False
                    
                    min_value = numeric_rules.get('min_value')
                    if min_value is not None and float(value) < min_value:
                        return False
                        
                    max_value = numeric_rules.get('max_value')
                    if max_value is not None and float(value) > max_value:
                        return False

                elif DataParser.is_string_value(value):
                    text_rules = data_type_rules.get('text', {})
                    str_value = str(value)
                    
                    min_length = text_rules.get('min_length', 1)
                    if len(str_value) < min_length:
                        return False
                        
                    max_length = text_rules.get('max_length')
                    if max_length is not None and len(str_value) > max_length:
                        return False

        return True

    @staticmethod
    def filtrarSegunExclusiones(datos: List[Dict[str, Any]], exclusiones: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Aplica reglas de exclusión a los datos
        :param datos: Datos a filtrar
        :param exclusiones: Configuración de exclusiones
        :return: Datos filtrados según exclusiones
        """
        if not exclusiones:
            return datos

        datos_filtrados = datos.copy()
        
        # Excluir columnas específicas
        columns_to_ignore = exclusiones.get('columns_to_ignore', [])
        if columns_to_ignore:
            datos_filtrados = [
                {k: v for k, v in row.items() if k not in columns_to_ignore}
                for row in datos_filtrados
            ]

        # Aplicar filtros de filas
        row_filters = exclusiones.get('row_filters', [])
        for filter_rule in row_filters:
            column = filter_rule.get('column')
            condition = filter_rule.get('condition')
            value = filter_rule.get('value')
            
            if column and condition and value is not None:
                if condition == 'equals':
                    datos_filtrados = [row for row in datos_filtrados if row.get(column) != value]
                elif condition == 'not_equals':
                    datos_filtrados = [row for row in datos_filtrados if row.get(column) == value]
                elif condition == 'contains':
                    datos_filtrados = [row for row in datos_filtrados if value not in str(row.get(column, ''))]
                elif condition == 'not_contains':
                    datos_filtrados = [row for row in datos_filtrados if value in str(row.get(column, ''))]

        return datos_filtrados

    @staticmethod
    def aplicarTransformaciones(datos: List[Dict[str, Any]], transformaciones: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Aplica reglas de transformación a los datos
        :param datos: Datos a transformar
        :param transformaciones: Lista de reglas de transformación
        :return: Datos transformados
        """
        if not transformaciones:
            return datos

        datos_transformados = []
        
        for row in datos:
            row_transformed = row.copy()
            
            for transform in transformaciones:
                column = transform.get('column')
                operation = transform.get('operation')
                params = transform.get('params', {})
                
                if column in row_transformed and operation:
                    original_value = row_transformed[column]
                    
                    try:
                        if operation == 'uppercase':
                            row_transformed[column] = str(original_value).upper()
                        elif operation == 'lowercase':
                            row_transformed[column] = str(original_value).lower()
                        elif operation == 'trim':
                            row_transformed[column] = str(original_value).strip()
                        elif operation == 'replace':
                            old = params.get('old', '')
                            new = params.get('new', '')
                            row_transformed[column] = str(original_value).replace(old, new)
                        elif operation == 'normalize_null':
                            if DataParser.is_null_value(original_value):
                                row_transformed[column] = None
                        elif operation == 'round_numeric':
                            if DataParser.is_numeric_value(original_value):
                                decimals = params.get('decimals', 2)
                                row_transformed[column] = round(float(original_value), decimals)
                    except (ValueError, TypeError):
                        # Keep original value if transformation fails
                        pass
            
            datos_transformados.append(row_transformed)
        
        return datos_transformados
