"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Lector de Ficheros CSV
AUTOR:       Fisherk2
FECHA:       2026-02-12
DESCRIPCIÓN: Lector de ficheros CSV que valida la existencia del fichero y su formato
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""
import os
import csv
from typing import List

class CSVReader:
    """
    Componente responsable de leer archivos CSV de forma segura
    """
    def validateFileExist (self, filepath: str) -> bool:
        """
        Verifica si el archivo existe en la ruta especificada
        :param filepath: Ruta absoluta o relativa del fichero
        :return: ¿El archivo existe?
        """
        return os.path.exists(filepath)

    def readHeaders(self, filepath: str) -> List[str]:
        """
        Lee solo los encabezados del archivo CSV
        :param filepath: Ruta absoluta o relativa del fichero
        :return: Lista de encabezados
        """
        if not self.validateFileExist(filepath):
            return []

        headers = []
        try:
            with open(filepath, 'r', newline='') as file:
                reader = csv.reader(file)
                firstRow = next(reader)

                # ■■■■■■■■■■■■■ En caso de que la primera fila pueda estar vacia ■■■■■■■■■■■■■
                if firstRow is not None:
                    headers = firstRow
        except(IOError):
            print(f"Error leyendo encabezados en el fichero {filepath}")
            return []
        except(UnicodeDecodeError):
            print(f"Error decodificando archivo {filepath}")
            return []
        return headers


# ▏▎▍▌▋▊▉▉▉▉▉▉▉▉ Pseudocodigo ▉▉▉▉▉▉▉▉▉▊▋▌▍▎▏


public
Iterator < Dict < String, String >> readRows(String
filePath)
"""
Lee las filas del archivo CSV como diccionarios
Retorna un iterador para procesamiento eficiente
"""
if !this.validateFileExists(filePath)
raise FileNotFoundError("El archivo no existe: " + filePath)

try
    with open(filePath, 'r', newline='') as file
        var
        reader = csv.DictReader(file)

        # Procesar fila por fila usando yield simulado con generador
        for row in reader
            yield row
catch
IOError
e
raise IOError("Error leyendo archivo CSV: " + str(e))
catch
UnicodeDecodeError
e
raise ValueError("Error decodificando archivo CSV: " + str(e))
catch
csv.Error
e
raise ValueError("Formato CSV inválido: " + str(e))

public
int
countRows(String
filePath)
"""
Cuenta el número total de filas en el archivo (excluyendo encabezados)
"""
if !this.validateFileExists(filePath)
return 0

var
count = 0

try
    with open(filePath, 'r', newline='') as file
        var
        reader = csv.reader(file)
        # Saltar encabezados
        next(reader, None)

        for row in reader
            count + +
catch
IOError
e
print("Error contando filas: " + str(e))
return 0

return count