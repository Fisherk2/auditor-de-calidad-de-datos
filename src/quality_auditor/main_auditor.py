"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Coordinador de todos los analisis de calidad de datos
AUTOR:       Fisherk2
FECHA:       2026-02-17
DESCRIPCIÓN: Proporciona un punto de entrada centralizado para todas las funciones de auditoría (Patrón Strategy)
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""
import math
from typing import Any, Optional
from datetime import datetime

from src.quality_auditor.null_analyzer import NullAnalyzer
from src.quality_auditor.uniqueness_analyzer import UniquenessAnalyzer
from src.quality_auditor.date_analyzer import DateAnalyzer
from src.quality_auditor.statistical_analyzer import StatisticalAnalyzer
from utils.data_parser import DataParser

# ⋮⋮⋮⋮⋮⋮⋮⋮ ALIAS de estructura datos ⋮⋮⋮⋮⋮⋮⋮⋮
RowDataType = list[dict[str, Any]]

class QualityAuditor:
    """
    Clase principal que coordina todos los análisis de calidad de datos
    Implementa el patrón Strategy al delegar diferentes tipos de análisis
    """

    @staticmethod
    def quality_audit(data: RowDataType) -> dict[str, Any]:
        """
        Realiza un análisis completo de calidad de datos
        :param data: Lista de diccionarios representando filas de datos
        :return: Diccionario con todos los resultados de calidad
        """
        # ■■■■■■■■■■■■■ Agregar timestamp del análisis ■■■■■■■■■■■■■
        results = dict()
        results["timestamp"] = datetime.now().isoformat()
        results["total_rows"] = len(data) if data else 0

        # ■■■■■■■■■■■■■ Analisis de nulos ■■■■■■■■■■■■■
        results["null_analysis"] = NullAnalyzer.count_nulls(data)

        # ■■■■■■■■■■■■■ Analisis de unicidad ■■■■■■■■■■■■■
        results["uniqueness_analysis"] = UniquenessAnalyzer.calculate_uniqueness(data)

        # ■■■■■■■■■■■■■ Analisis estadistico ■■■■■■■■■■■■■
        results["statistical_analysis"] = StatisticalAnalyzer.summary_stadistic(data)

        # ■■■■■■■■■■■■■ Informacion adicional de tipos ■■■■■■■■■■■■■
        results["count_types"] = StatisticalAnalyzer.count_by_type(data)

        return results

    @staticmethod
    def advance_quality_audit(
            data: RowDataType,
            birth_column_name: Optional[str] = None,
            numerics_columns: Optional[list[str]] = None,
            text_columns: Optional[list[str]] = None
    ) -> dict[str, Any]:
        """
        Realiza un analisis completo de calidad de datos con opciones avanzadas
        :param data: Lista de diccionarios representando filas de datos
        :param birth_column_name: Columna especifica para analisis de coherencia de fechas
        :param numerics_columns: Lista de columnas a tratar como nuemricas
        :param text_columns: Lista de columnas a tratar como de texto
        :return: Diccionario con todos los resultados de calidad ampliados
        """
        results = QualityAuditor.quality_audit(data)

        # ■■■■■■■■■■■■■ Analisis de fechas si se especifica una columna ■■■■■■■■■■■■■
        if birth_column_name is not None and birth_column_name.strip():
            date_errors = DateAnalyzer.check_date_coherence(data, birth_column_name)
            results["date_analysis"] = dict()
            results["date_analysis"]["date_column"] = birth_column_name
            results["date_analysis"]["errors"] = date_errors
            results["date_analysis"]["error_total"] = len(date_errors)

        # ■■■■■■■■■■■■■ Analisis estadistico detallado si se especifican columnas numericas ■■■■■■■■■■■■■
        if numerics_columns is not None and numerics_columns:
            numerics_values = StatisticalAnalyzer.get_numerics_values(data)
            statistics_details = dict()
            for column in numerics_columns:
                if column in numerics_values.keys():
                    values = numerics_values[column]
                    stadistics = dict()

                    # ▲▲▲▲▲▲ Calcular percentiles ▲▲▲▲▲▲
                    if values:
                        sorted_values = sorted(values)
                        size = len(values)

                        stadistics["min"] = sorted_values[0]
                        stadistics["max"] = sorted_values[size - 1]
                        stadistics["media"] = sum(sorted_values) / size

                        # # ▲▲▲▲▲▲ Calcular mediana ▲▲▲▲▲▲
                        half = size // 2
                        if size % 2 == 0:
                            stadistics["mediana"] = (sorted_values[half - 1] + sorted_values[half]) / 2.0
                        else:
                            stadistics["mediana"] = sorted_values[half]

                        # ▲▲▲▲▲▲ Percentiles ▲▲▲▲▲▲
                        stadistics["q25"] = sorted_values[math.floor(size * 0.25)]
                        stadistics["q75"] = sorted_values[math.floor(size * 0.75)]

                    statistics_details[column] = stadistics

            results["statistical_details"] = statistics_details

        # ■■■■■■■■■■■■■ Análisis detallado de columnas de texto si se especifican ■■■■■■■■■■■■■
        if text_columns is not None and text_columns:
            text_analysis = dict()
            for column in text_columns:
                text_values = list()

                # ▲▲▲▲▲▲ Recoger valores de texto de la columna ▲▲▲▲▲▲
                for row in data:
                    if column in row.keys():
                        value = row[column]
                        if DataParser.is_string_value(value):
                            text_values.append(str(value))
                if text_values:
                    text_metrics = dict()

                    # ▲▲▲▲▲▲ Logitud promedio de texto ▲▲▲▲▲▲
                    total_lenght = 0
                    for text in text_values:
                        total_lenght += len(text)

                    text_metrics["total_registers"] = len(text_values)
                    text_metrics["average_lenght"] = round(total_lenght / len(text_values), 2)

                    # ▲▲▲▲▲▲ Logitud minima y maxima ▲▲▲▲▲▲
                    lenghts = list()
                    for text in text_values:
                        lenghts.append(len(text))
                    text_metrics["max_lenght"] = max(lenghts)
                    text_metrics["min_lenght"] = min(lenghts)

                    # ▲▲▲▲▲▲ Contar valores unicos ▲▲▲▲▲▲
                    unique_values = set(text_values)
                    text_metrics["unique_values"] = len(unique_values)
                    text_metrics["unique_percent"] = round(len(unique_values) / len(text_values) * 100.0, 2)

                    # ▲▲▲▲▲▲ Detectar posible problemas de formato ▲▲▲▲▲▲
                    format_problems = list()
                    for text in text_values:
                        # ▲▲▲▲▲▲ Detectar cadenas con solo espacios ▲▲▲▲▲▲
                        if not (text.strip()) and text:
                            format_problems.append("Cadenas con solo espacio")
                            break
                    text_metrics["format_problems"] = format_problems
                    text_metrics["has_issues"] = len(format_problems) > 0

                    text_analysis[column] = text_metrics

            results["text_analysis"] = text_analysis

        return results

    @staticmethod
    def get_general_metrics(data: RowDataType) -> dict[str, int]:
        """
        Obtiene metricas generales de calidad de datos
        :param data: Lista de diccionarios representando filas de datos
        :return: Diccionario con metricas generales de calidad
        """
        metrics = dict()
        if data is None or not data:
            metrics["total_rows"] = 0
            metrics["total_columns"] = 0
            metrics["general_quality"] = 0.0
            return metrics

        # ■■■■■■■■■■■■■ Obtener informacion basica ■■■■■■■■■■■■■
        nulls_count = NullAnalyzer.count_nulls(data)
        rows_total_count = len(data)

        # ■■■■■■■■■■■■■ Calcular metricas ■■■■■■■■■■■■■
        metrics["total_rows"] = rows_total_count
        metrics["total_columns"] = len(nulls_count.keys())

        # ■■■■■■■■■■■■■ Calcular calidad general basada en nulos ■■■■■■■■■■■■■
        nulls_total = 0
        for count in nulls_count.values():
            nulls_total += count

        posible_nulls_total = rows_total_count * len(nulls_count.keys())
        nulls_percent = 0.0
        if posible_nulls_total > 0:
            nulls_percent = (nulls_total / posible_nulls_total) * 100.0
        metrics["nulls_percent"] = round(nulls_percent, 2)
        metrics["general_quality"] = round(100.0 - nulls_percent, 2)

        # ■■■■■■■■■■■■■ Metricas de unicidad ■■■■■■■■■■■■■
        uniqueness = UniquenessAnalyzer.calculate_uniqueness(data)
        average_uniqueness = 0.0
        if uniqueness:
            sum_uniqueness = 0.0
            for value in uniqueness.values():
                sum_uniqueness += value
            average_uniqueness = sum_uniqueness / len(uniqueness)
        metrics["average_uniqueness"] = round(average_uniqueness, 2)

        return metrics

    @staticmethod
    def generate_alerts(
            data: RowDataType,
            null_umbral: Optional[float] = 50.0,
            low_uniqueness_umbral: Optional[float] = 10.0,
            high_uniqueness_umbral: Optional[float] = 95.0
    ) -> list[str]:
        """
        Genera alertas basadas en umbrales de calidad
        :param data: Lista de diccionarios representando filas de datos
        :param null_umbral: Porcentaje de nulos que dispara alerta
        :param low_uniqueness_umbral: Porcentaje de unicidad baja que dispara alerta
        :param high_uniqueness_umbral: Porcentaje de unicidad alta que dispara alerta
        :return: Lista de mensajes de alerta
        """
        alerts = list()
        if data is None or not data:
            alerts.append("ALERTA: No hay datos para analizar")
            return alerts

        # ■■■■■■■■■■■■■ Analisis de nulos ■■■■■■■■■■■■■
        count_nulls = NullAnalyzer.count_nulls(data)
        total_rows = len(data)
        for column in count_nulls.keys():
            nulls = count_nulls[column]
            percent_nulls = (nulls / total_rows) * 100.0
            if percent_nulls >= null_umbral:
                message = f"""
                ALERTA: Columna '{column}' tiene {round(percent_nulls, 2)}% de valores nulos
                (umbral: {null_umbral}%)
                """
                alerts.append(message)

        # ■■■■■■■■■■■■■ Analisis de unicidad ■■■■■■■■■■■■■
        uniqueness = UniquenessAnalyzer.calculate_uniqueness(data)
        for column in uniqueness.keys():
            percent_uniqueness = uniqueness[column]
            if percent_uniqueness <= low_uniqueness_umbral:
                message = f"""
                ALERTA: Columna '{column}' tiene baja unicidad: {round(percent_uniqueness, 2)}%
                (umbral bajo: {low_uniqueness_umbral}%)
                """
                alerts.append(message)
            elif percent_uniqueness >= high_uniqueness_umbral:
                message = f"""
                ALERTA: Columna '{column}' tiene alta unicidad: {round(percent_uniqueness, 2)}%
                (umbral alto: {high_uniqueness_umbral}%)
                """
                alerts.append(message)

        return alerts
