"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Utilidades reutilizables para manejo de fechas
AUTOR:       Fisherk2
FECHA:       2026-02-10
DESCRIPCIÓN: Componente de bajo nivel que proporciona funciones auxiliares para conversión y validación de fechas
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""

import datetime

class DateHelper:
    """
    Clase de utilidad para operaciones comunes con fechas
    """

    def is_valid_date_format (self, date:str, format:str = "%Y-%m-%d") -> bool:
        """
        Valida si un string tiene el formato de fecha especificado
        :param date: fecha en forma de cadena
        :param format: Formato de fecha especificado
        :return: ¿Tiene el formato de fecha especificado correcto?
        """
        try:
            datetime.datetime.strptime(date, format)
            return True
        except ValueError:
            return False


# ▼△▼△▼△▼△▼△▼△▼△▼△▼△ Pseudocodigo △▼△▼△▼△▼△▼△▼△▼△▼△▼

public
static
Optional[datetime.datetime]
parseDate(String
dateString, String
format = "%Y-%m-%d")
"""
Convierte un string a objeto datetime según el formato especificado
"""
try
    return datetime.datetime.strptime(dateString, format)
catch
ValueError
e
return null

public
static
boolean
isFutureDate(datetime.datetime
date)
"""
Verifica si una fecha es futura comparándola con la fecha actual
"""
var
currentDate = datetime.datetime.now()
return date > currentDate

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