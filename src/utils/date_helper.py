"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Utilidades reutilizables para manejo de fechas
AUTOR:       Fisherk2
FECHA:       2026-02-10
DESCRIPCIÓN: Componente de bajo nivel que proporciona funciones auxiliares para conversión y validación de fechas
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""

import datetime
from typing import Optional

class DateHelper:
    """
    Clase de utilidad para operaciones comunes con fechas
    """

    @staticmethod
    def is_valid_date_format (date:str, format:str = "%Y-%m-%d") -> bool:
        """
        Valida si un string tiene el formato de fecha especificado
        :param date: Fecha en forma de cadena
        :param format: Formato de fecha especificado
        :return: ¿Tiene el formato de fecha especificado correcto?
        """
        try:
            datetime.datetime.strptime(date, format)
            return True
        except ValueError:
            return False

    @staticmethod
    def parse_date(date: str, format: str = "%Y-%m-%d") -> Optional[datetime.datetime]:
        """
        Convierte un string a objeto datetime segun el formato especificado
        :param date: Fecha en forma de cadena
        :param format: Formato de fecha especificado
        :return: datetime o None si hay error
        """
        try:
            return datetime.datetime.strptime(date, format)
        except ValueError:
            return None

    @staticmethod
    def is_future_date(date: datetime.datetime) -> bool:
        """
        Verifica si una fecha es futura conparandola con la fecha actual
        :param date:
        :return:
        """
        current_date = datetime.datetime.now()
        return date > current_date


# ▼△▼△▼△▼△▼△▼△▼△▼△▼△ Pseudocodigo △▼△▼△▼△▼△▼△▼△▼△▼△▼

public
static
boolean
isDateBefore(datetime.datetime
date1, datetime.datetime
date2)
"""
Verifica si la primera fecha es anterior a la segunda
"""
return date1 < date2

public
static
String
formatDate(datetime.datetime
date, String
format = "%Y-%m-%d")
"""
Formatea un objeto datetime a string según el formato especificado
"""
return date.strftime(format)

public
static
List[String]
getSupportedFormats()
"""
Retorna lista de formatos de fecha soportados comúnmente
"""
var
formats = list()
formats.append("%Y-%m-%d")  # 2023-12-25
formats.append("%d/%m/%Y")  # 25/12/2023
formats.append("%m/%d/%Y")  # 12/25/2023
formats.append("%Y-%m-%d %H:%M:%S")  # 2023-12-25 14:30:00
formats.append("%d/%m/%Y %H:%M")  # 25/12/2023 14:30
return formats