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
from typing import Iterator


class CSVReader:
    """
    Componente responsable de leer archivos CSV de forma segura
    """

    def validate_file_exist(self, filepath: str) -> bool:
        """
        Verifica si el archivo existe en la ruta especificada
        :param filepath: Ruta absoluta o relativa del fichero
        :return: ¿El archivo existe?
        """
        return os.path.exists(filepath)

    def read_headers(self, filepath: str) -> list[str]:
        """
        Lee solo los encabezados del archivo CSV
        :param filepath: Ruta absoluta o relativa del fichero
        :return: Lista de encabezados
        """
        if not self.validate_file_exist(filepath):
            return []

        headers = []
        try:
            with open(filepath, 'r', newline='') as file:
                reader = csv.reader(file)
                first_row = next(reader)

                # ■■■■■■■■■■■■■ En caso de que la primera fila pueda estar vacia ■■■■■■■■■■■■■
                if first_row is not None:
                    headers = first_row

        except IOError:
            print(f"Error leyendo encabezados en el fichero {filepath}")
            return []
        except UnicodeDecodeError:
            print(f"Error decodificando archivo {filepath}")
            return []
        return headers

    def read_rows(self, filepath: str) -> Iterator[dict[str, str]]:
        """
        Lee las filas del archivo CSV como diccionarios
        :param filepath: Ruta absoluta o relativa del fichero
        :return: Iterador para procesar las filas eficientemente
        """
        if not self.validate_file_exist(filepath):
            raise FileNotFoundError(f"El archivo no existe: {filepath}")

        try:
            with open(filepath, 'r', newline='') as file:
                reader = csv.DictReader(file)

                # ■■■■■■■■■■■■■ Procesar fila por fila usando yield simulado con generador ■■■■■■■■■■■■■
                for row in reader:
                    yield row

        except IOError:
            print(f"Error leyendo archivo CSV {filepath}")
        except UnicodeDecodeError:
            raise ValueError(f"Error decodificando archivo CSV {filepath}")
        except csv.Error:
            raise ValueError(f"Formato CSV invalido en {filepath}")

    def count_rows(self, filepath) -> int:
        """
        Cuenta el numero total de filas en el archivo (Excluyendo encabezados)
        :param filepath: Ruta absoluta o relativo del fichero
        :return: Numero total de filas del fichero.
        """
        if not self.validate_file_exist(filepath):
            return 0

        count = 0

        try:
            with open(filepath, 'r', newline='') as file:
                reader = csv.reader(file)

                # ■■■■■■■■■■■■■ Saltar encabezado ■■■■■■■■■■■■■
                next(reader, None)

                for row in reader:
                    count += 1

        except IOError:
            print(f"Error contando filas: {filepath}")
            return 0

        return count