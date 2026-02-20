"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Parseo y validación básica de datos de entrada
AUTOR:       Fisherk2
FECHA:       2026-02-16
DESCRIPCIÓN: Capa de acceso a datos que proporciona funciones para validar y transformar datos de entrada
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""

from typing import Any

# ⋮⋮⋮⋮⋮⋮⋮⋮ ALIAS de estructura datos ⋮⋮⋮⋮⋮⋮⋮⋮
RowDataType = list[dict[str, Any]]
ColumnIndexMap = dict[str, list[int]]


class DataParser:
    """
    Clase de utilidad para parseo y validación de datos estructurados
    """

    @staticmethod
    def is_numeric_value(value: Any, numeric_rules: dict[str, Any] = None) -> bool:
        """
        Verifica si un valor puede ser convertido a número según reglas
        :param value: Valor a evaluar
        :param numeric_rules: Reglas de configuración para tipo numérico (opcional)
        :return: ¿Es un valor numérico válido según reglas?
        """
        if value is None:
            return False
        if isinstance(value, (int, float)):
            num_value = float(value)

            # ■■■■■■■■■■■■■ Verificar reglas de valores permitidos ■■■■■■■■■■■■■
            if numeric_rules:
                if not numeric_rules.get('allow_negative', True) and num_value < 0:
                    return False
                min_value = numeric_rules.get('min_value')
                if min_value is not None and num_value < min_value:
                    return False
                max_value = numeric_rules.get('max_value')
                if max_value is not None and num_value > max_value:
                    return False
            return True

        if isinstance(value, str):
            try:
                num_value = float(value)

                # ■■■■■■■■■■■■■ Verificar reglas de valores permitidos ■■■■■■■■■■■■■
                if numeric_rules:
                    if not numeric_rules.get('allow_negative', True) and num_value < 0:
                        return False
                    min_value = numeric_rules.get('min_value')
                    if min_value is not None and num_value < min_value:
                        return False
                    max_value = numeric_rules.get('max_value')
                    if max_value is not None and num_value > max_value:
                        return False
                return True
            except ValueError:
                return False
        return False

    @staticmethod
    def is_string_value(value: Any, text_rules: dict[str, Any] = None) -> bool:
        """
        Verifica si un valor es una cadena válida según reglas
        :param value: Valor a evaluar
        :param text_rules: Reglas de configuración para tipo texto (opcional)
        :return: ¿Es una cadena válida según reglas?
        """
        if value is None:
            return False
        if isinstance(value, str):
            str_value = str(value)

            # ■■■■■■■■■■■■■ Verificar reglas de longitud ■■■■■■■■■■■■■
            if text_rules:
                min_length = text_rules.get('min_length', 1)
                if len(str_value) < min_length:
                    return False
                max_length = text_rules.get('max_length')
                if max_length is not None and len(str_value) > max_length:
                    return False

                # ■■■■■■■■■■■■■ Verificar si permite cadenas vacias ■■■■■■■■■■■■■
                if not text_rules.get('allow_empty_strings', False) and len(str_value.strip()) == 0:
                    return False
                return len(str_value.strip()) > 0
            else:
                # Sin reglas: cualquier string no vacío es válido
                return len(str_value.strip()) > 0

        return False

    @staticmethod
    def is_bool_value(value: Any, boolean_rules: dict[str, Any] = None) -> bool:
        """
        Verifica si un valor puede ser interpretado como booleano según reglas
        :param value: Valor a evaluar
        :param boolean_rules: Reglas de configuración para tipo booleano (opcional)
        :return: ¿Es un valor booleano válido según reglas?
        """
        if value is None:
            return False
        if isinstance(value, bool):
            return True
        if isinstance(value, str):
            lower_value = value.lower().strip()

            # ■■■■■■■■■■■■■ Usar interpretaciones configuradas ■■■■■■■■■■■■■
            if boolean_rules:
                supported_interpretations = boolean_rules.get('supported_interpretations',
                                                              ['true', 'false', '1', '0', 'yes', 'no', 'on', 'off'])
                return lower_value in supported_interpretations
            else:
                return lower_value in ['true', 'false', '1', '0', 'yes', 'no', 'on', 'off']

        return False

    @staticmethod
    def is_null_value(value: Any, null_rules: dict[str, Any] = None) -> bool:
        """
        Verifica si un valor es nulo o representa un valor nulo según reglas
        :param value: Valor a evaluar
        :param null_rules: Reglas de configuración para tipo nulo (opcional)
        :return: ¿Es un valor nulo según reglas?
        """
        if value is None:
            return True
        if isinstance(value, str):
            trimmed = value.lower().strip()

            # ■■■■■■■■■■■■■ Usar interpretaciones configuradas ■■■■■■■■■■■■■
            if null_rules:
                supported_interpretations = null_rules.get('supported_interpretations',
                                                           ['', 'null', 'none', 'na', 'n/a', '<null>'])
                return trimmed in supported_interpretations
            else:
                return trimmed in ['', 'null', 'none', 'na', 'n/a', '<null>']

        return False

    @staticmethod
    def thresholds_filter(data: RowDataType, exclusions: dict[str, Any]) -> RowDataType:
        """
        Aplica reglas de exclusión a los datos
        :param data: Datos a filtrar
        :param exclusions: Configuración de exclusiones
        :return: Datos filtrados según exclusiones
        """
        if not exclusions:
            return data

        datos_filtrados = data.copy()

        # ■■■■■■■■■■■■■ Excluir columnas especificas ■■■■■■■■■■■■■
        columns_to_ignore = exclusions.get('columns_to_ignore', [])
        if columns_to_ignore:
            datos_filtrados = [
                {k: v for k, v in row.items() if k not in columns_to_ignore}
                for row in datos_filtrados
            ]

        # ■■■■■■■■■■■■■ Aplicar filtros de filas ■■■■■■■■■■■■■
        row_filters = exclusions.get('row_filters', [])
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

        # TODO: ▏▎▍▌▋▊▉▉▉▉▉▉▉▉ file_patterns_to_ignore se maneja a nivel de archivos, no de filas ▉▉▉▉▉▉▉▉▉▊▋▌▍▎▏
        # Este parámetro debe ser procesado antes de leer los datos del archivo
        # Ejemplo de uso: archivos que coincidan con patrones como "*_temp.csv", "test_*.csv", etc.

        return datos_filtrados

    @staticmethod
    def transform_data(data: RowDataType, data_types_rules: dict[str, Any]) -> RowDataType:
        """
        Transforma datos según tipos detectados por los métodos de validación
        :param data: Datos a transformar
        :param data_types_rules: Reglas de configuración para tipos de datos
        :return: Datos transformados con tipos consistentes
        """
        if data is None or not data:
            return []

        datos_transformados = []

        for row in data:
            row_transformed = row.copy()

            for column, value in row_transformed.items():
                # Obtener reglas específicas para cada tipo
                numeric_rules = data_types_rules.get('numeric', {})
                text_rules = data_types_rules.get('text', {})
                boolean_rules = data_types_rules.get('boolean', {})
                null_rules = data_types_rules.get('null', {})

                # ■■■■■■■■■■■■■ Transformar a tipo númerico si es posible ■■■■■■■■■■■■■
                if DataParser.is_numeric_value(value, numeric_rules):
                    try:
                        # ▲▲▲▲▲▲ Convertir a float, luego a int si no tiene decimales ▲▲▲▲▲▲
                        num_value = float(value)

                        if num_value.is_integer():
                            row_transformed[column] = int(num_value)
                        else:
                            row_transformed[column] = num_value
                    except (ValueError, TypeError):
                        # ▲▲▲▲▲▲ Mantener original si falla conversion ▲▲▲▲▲▲
                        pass

                # ▲▲▲▲▲▲ Transformar a booleano si es posible ▲▲▲▲▲▲
                elif DataParser.is_bool_value(value, boolean_rules):
                    if isinstance(value, bool):
                        row_transformed[column] = value
                    elif isinstance(value, str):
                        lower_value = value.lower().strip()
                        supported_interpretations = boolean_rules.get(
                            'supported_interpretations',
                            ['true', 'false', '1', '0', 'yes', 'no', 'on', 'off']
                        )
                        if lower_value in supported_interpretations[:len(supported_interpretations) // 2]:
                            row_transformed[column] = True
                        else:
                            row_transformed[column] = False

                # ▲▲▲▲▲▲ Normalizar valores nulos ▲▲▲▲▲▲
                elif DataParser.is_null_value(value, null_rules):
                    row_transformed[column] = None

                # ▲▲▲▲▲▲ Mantener strings válidos como están ▲▲▲▲▲▲
                elif DataParser.is_string_value(value, text_rules):
                    row_transformed[column] = str(value).strip()

            datos_transformados.append(row_transformed)

        return datos_transformados
