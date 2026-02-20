"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Utilidades reutilizables para manejo de fechas
AUTOR:       Fisherk2
FECHA:       2026-02-19
DESCRIPCIÓN: Componente de bajo nivel que proporciona funciones auxiliares para operaciones con fechas
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""
import datetime
from typing import Optional, Any
from src.readers.quality_rules_reader import QualityRulesReader

class DateHelper:
    """
    Clase de utilidad para operaciones comunes con fechas
    Integrada con sistema de configuración de reglas de calidad
    """

    @staticmethod
    def is_valid_date_format(date: str, date_format: str = "%Y-%m-%d") -> bool:
        """
        Valida si un string tiene el formato de fecha especificado
        :param date: Fecha en forma de cadena
        :param date_format: Formato de fecha especificado
        :return: ¿Tiene el formato de fecha especificado correcto?
        """
        try:
            datetime.datetime.strptime(date, date_format)
            return True
        except ValueError:
            return False

    @staticmethod
    def parse_date(date: str, date_format: str = "%Y-%m-%d") -> Optional[datetime.datetime]:
        """
        Convierte un string a objeto datetime segun el formato especificado
        :param date: Fecha en forma de cadena
        :param date_format: Formato de fecha especificado
        :return: datetime o None si hay error
        """
        try:
            return datetime.datetime.strptime(date, date_format)
        except ValueError:
            return None

    @staticmethod
    def is_future_date(date: datetime.datetime) -> bool:
        """
        Verifica si una fecha es futura
        :param date: Fecha a evaluar
        :return: ¿Es fecha futura?
        """
        current_date = datetime.datetime.now()
        return date > current_date

    @staticmethod
    def is_date_before(first_date: datetime.datetime, second_date: datetime.datetime) -> bool:
        """
        Verifica si la primer fecha es anterior a la segunda
        :param first_date:
        :param second_date:
        :return: ¿La primer fecha es anterior a la segunda?
        """
        return first_date < second_date

    @staticmethod
    def format_date(date: datetime.datetime, date_format: str = "%Y-%m-%d") -> str:
        """
        Formatea un objeto datetime a string según el formato especificado
        :param date: Fecha en forma de cadena
        :param date_format: Formato de fecha especificado
        :return: Fecha en forma de cadena
        """
        return date.strftime(date_format)

    @staticmethod
    def get_supported_formats(path_quality_rules: Optional[str] = None) -> list[str]:
        """
        Retorna lista de formatos de fecha soportados desde configuración
        :param path_quality_rules: Ruta opcional al archivo YAML de configuración
        :return: Lista de formatos de fecha configurados
        """
        date_rules = DateHelper.get_date_rules(path_quality_rules)
        return date_rules.get('supported_formats', ["%Y-%m-%d"])

    @staticmethod
    def get_date_rules(path_quality_rules: Optional[str]) -> dict[str, Any]:
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