"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Análisis de fechas
AUTOR:       Fisherk2
FECHA:       2026-02-19
DESCRIPCIÓN: Proporciona funciones para verificar coherencia de fechas (ej: fecha_nacimiento > fecha_actual)
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""

from typing import Any, Optional
from datetime import datetime
from src.utils.date_helper import DateHelper
from src.readers.quality_rules_reader import QualityRulesReader

# ⋮⋮⋮⋮⋮⋮⋮⋮ ALIAS de estructura datos ⋮⋮⋮⋮⋮⋮⋮⋮
RowDataType = list[dict[str, Any]]


class DateAnalyzer:
    """
    Clase para análisis de coherencia y validación de fechas en datos estructurados
    """

    @staticmethod
    def check_date_coherence(
            datos: RowDataType,
            birth_column_name: str,
            path_quality_rules: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Verifica la coherencia de fechas usando configuración
        Detecta fechas de nacimiento futuras o fechas imposibles según reglas configuradas
        :param datos: Lista de diccionarios representando filas de datos
        :param birth_column_name: Nombre de la columna que contiene fechas de nacimiento
        :param path_quality_rules: Ruta opcional al archivo YAML de configuración
        :return: Diccionario con errores y reglas aplicadas
        """
        if datos is None or not datos:
            return {"errors": [], "rules_applied": {}}

        errors = list()
        rules_applied = dict()

        if birth_column_name is None or not birth_column_name.strip():
            errors.append("Error en encabezado: Nombre de columna de fecha inválido o vacío")
            return {"errors": errors, "rules_applied": rules_applied}

        # ■■■■■■■■■■■■ Cargar configuración de fechas ■■■■■■■■■■■■■
        date_rules = DateAnalyzer._get_date_rules(path_quality_rules)
        supported_formats = date_rules.get('supported_formats', ["%Y-%m-%d"])
        allow_future = date_rules.get('allow_future_dates', False)
        min_date_str = date_rules.get('min_date')
        max_date_str = date_rules.get('max_date')

        # ■■■■■■■■■■■■ Guardar reglas aplicadas ■■■■■■■■■■■■■
        rules_applied["supported_formats"] = supported_formats
        rules_applied["allow_future_dates"] = allow_future
        rules_applied["min_date"] = min_date_str
        rules_applied["max_date"] = max_date_str

        # ■■■■■■■■■■■■ Parsear fechas de rango si existen ■■■■■■■■■■■■■
        min_date = None
        max_date = None

        if min_date_str:
            try:
                min_date = datetime.strptime(min_date_str, '%Y-%m-%d')
            except ValueError:
                errors.append(f"Advertencia: Fecha mínima inválida en configuración: {min_date_str}")

        if max_date_str:
            try:
                max_date = datetime.strptime(max_date_str, '%Y-%m-%d')
            except ValueError:
                errors.append(f"Advertencia: Fecha máxima inválida en configuración: {max_date_str}")

        for i in range(len(datos)):
            row = datos[i]

            if not birth_column_name in row.keys():
                errors.append(f"Fila {str(i + 1)}: Columna '{birth_column_name}' no encontrada")
                continue

            # ■■■■■■■■■■■■■ Saltar valores nulos, el análisis de nulos se hace en otro módulo ■■■■■■■■■■■■■
            date_value = row[birth_column_name]
            if date_value is None:
                continue

            date: str = ""

            if isinstance(date_value, str):
                date: str = date_value.strip()
            else:
                date: str = str(date_value).strip()

            # ■■■■■■■■■■■■■ Saltar cadenas vacias ■■■■■■■■■■■■■
            if not date:
                continue

            # ■■■■■■■■■■■■■ Intentar parsear la fecha con diferentes formatos ■■■■■■■■■■■■■
            date_parsed = None
            for supported_format in supported_formats:
                date_parsed = DateHelper.parse_date(date, supported_format)
                if date_parsed is not None:
                    break

            if date_parsed is None:
                errors.append(f"Fila {i + 1}: Fecha invalida en columna '{birth_column_name}': {date}")

            # ■■■■■■■■■■■■■ Verificar reglas adicionales ■■■■■■■■■■■■■
            else:
                # ▲▲▲▲▲ Verificar si la fecha es futura ▲▲▲▲▲▲
                if not allow_future and DateHelper.is_date_before(datetime.now(), date_parsed):
                    mensaje = f"""
                    Fila {i + 1}: 
                    Fecha futura en columna '{birth_column_name}': {DateHelper.format_date(date_parsed, "%Y-%m-%d")} 
                    (actual: {DateHelper.format_date(datetime.now(), "%Y-%m-%d")})
                    """
                    errors.append(mensaje)

                # ▲▲▲▲▲ Verificar rango minimo ▲▲▲▲▲▲
                if min_date is not None and DateHelper.is_date_before(date_parsed, min_date):
                    message = f"""
                    Fila {i + 1}: Fecha fuera de rango minimo en '{birth_column_name}': {DateHelper.format_date(date_parsed, "%Y-%m-%d")}
                    (minimo permitido: {DateHelper.format_date(min_date, "%Y-%m-%d")})
                    """
                    errors.append(message)

                # ▲▲▲▲▲ Verificar rango maximo ▲▲▲▲▲▲
                if max_date is not None and DateHelper.is_date_before(max_date, date_parsed):
                    message = f"""
                    Fila {i + 1}: Fecha fuera de rango maximo en '{birth_column_name}': {DateHelper.format_date(date_parsed, "%Y-%m-%d")}
                    (maximo permitido: {DateHelper.format_date(max_date, "%Y-%m-%d")})
                    """
                    errors.append(message)

        return {"errors": errors, "rules_applied": rules_applied}

    @staticmethod
    def check_date_range(
            datos: RowDataType,
            column_name: str,
            minimum_date: Optional[datetime] = None,
            maximum_date: Optional[datetime] = None
    ) -> list[str]:
        """
        Verifica que las fechas esten dentro de un rango especifico
        :param datos: Lista de diccionarios representando filas de datos
        :param column_name: Nombre de la columna que contiene las fechas
        :param minimum_date: Fecha minimia permitida (Opcional)
        :param maximum_date: Fecha maxima permitida (Opcional)
        :return: Lista de mensajes de error indicando fechas fuera de rango
        """
        if datos is None or not datos:
            return list()

        errors = list()

        if column_name is None or not column_name.strip():
            errors.append("Error en encabezado: Nombre de columna de fecha inválido o vacío")
            return errors

        supported_formats = DateHelper.get_supported_formats()

        for i in range(len(datos)):
            row = datos[i]

            # ■■■■■■■■■■■■■ Saltar filas sin la columna ■■■■■■■■■■■■■
            if not column_name in row.keys():
                continue

            # ■■■■■■■■■■■■■ Saltar valores nulos ■■■■■■■■■■■■■
            date_value = row[column_name]
            if date_value is None:
                continue

            date: str = ""

            if isinstance(date_value, str):
                date = date_value.strip()
            else:
                date = str(date_value).strip()

            # ■■■■■■■■■■■■■ Saltar cadenas vacias ■■■■■■■■■■■■■
            if not date:
                continue

            # ■■■■■■■■■■■■■ Intentar parsear la fecha ■■■■■■■■■■■■■
            date_parsed = None
            for supported_format in supported_formats:
                date_parsed = DateHelper.parse_date(date, supported_format)
                if date_parsed is not None:
                    break

            if date_parsed is not None:

                # ▲▲▲▲▲▲ Verificar rango minimo ▲▲▲▲▲▲
                if minimum_date is not None and DateHelper.is_date_before(date_parsed, minimum_date):
                    message = f"""
                    Fila {i + 1}: Fecha fuera de rango minimo en '{column_name}': {DateHelper.format_date(date_parsed, "%Y-%m-%d")}
                    (minimo permitido: {DateHelper.format_date(minimum_date, "%Y-%m-%d")})
                    """
                    errors.append(message)

                # ▲▲▲▲▲▲ Verificar rango maximo ▲▲▲▲▲▲
                if maximum_date is not None and DateHelper.is_date_before(maximum_date, date_parsed):
                    message = f"""
                    Fila {i + 1}: Fecha fuera de rango maximo en '{column_name}': {DateHelper.format_date(date_parsed, "%Y-%m-%d")}
                    (maximo permitido: {DateHelper.format_date(maximum_date, "%Y-%m-%d")})
                    """
                    errors.append(message)

        return errors

    @staticmethod
    def _get_date_rules(path_quality_rules: Optional[str]) -> dict[str, Any]:
        """
        Obtiene las reglas de fechas desde configuración o valores por defecto
        :param path_quality_rules: Ruta opcional al archivo YAML de configuración
        :return: Diccionario con reglas de fechas
        """
        if path_quality_rules:
            try:
                config = QualityRulesReader.load_configs(path_quality_rules)
                return QualityRulesReader.get_data_type_rules(config, 'date')
            except (FileNotFoundError, ValueError, Exception):

                # ■■■■■■■■■■■■■ Si hay error, usar valores por defecto ■■■■■■■■■■■■■
                pass

        # ■■■■■■■■■■■■■ Valores por defecto si no hay configuración ■■■■■■■■■■■■■
        default_config = QualityRulesReader.apply_default_rules()
        return QualityRulesReader.get_data_type_rules(default_config, 'date')
