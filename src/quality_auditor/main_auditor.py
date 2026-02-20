"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Coordinador de todos los analisis de calidad de datos
AUTOR:       Fisherk2
FECHA:       2026-02-19
DESCRIPCIÓN: Proporciona un punto de entrada centralizado para todas las funciones de auditoría (Patrón Strategy)
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""
import math
from typing import Any, Optional
from datetime import datetime

from quality_auditor.null_analyzer import NullAnalyzer
from quality_auditor.uniqueness_analyzer import UniquenessAnalyzer
from quality_auditor.date_analyzer import DateAnalyzer
from quality_auditor.statistical_analyzer import StatisticalAnalyzer
from readers.quality_rules_reader import QualityRulesReader
from utils.data_parser import DataParser

# ⋮⋮⋮⋮⋮⋮⋮⋮ ALIAS de estructura datos ⋮⋮⋮⋮⋮⋮⋮⋮
RowDataType = list[dict[str, Any]]


class QualityAuditor:
    """
    Clase principal que coordina todos los análisis de calidad de datos
    Implementa el patrón Strategy al delegar diferentes tipos de análisis
    """

    @staticmethod
    def quality_audit(data: RowDataType, path_quality_rules: Optional[str] = None) -> dict[str, Any]:
        """
        Realiza un análisis completo de calidad de datos usando configuración
        :param data: Lista de diccionarios representando filas de datos
        :param path_quality_rules: Ruta opcional al archivo YAML de configuración
        :return: Diccionario con todos los resultados de calidad y reglas aplicadas
        """
        # ■■■■■■■■■■■■■ Agregar timestamp del análisis ■■■■■■■■■■■■■
        results = dict()
        results["timestamp"] = datetime.now().isoformat()
        results["total_rows"] = len(data) if data is not None else 0

        # ■■■■■■■■■■■■■ Cargar configuración y aplicar exclusiones ■■■■■■■■■■■■■
        config = QualityAuditor._load_configuration(path_quality_rules)
        filtered_data = QualityAuditor._apply_exclusions(data, config)

        results["config_applied"] = {
            "path_quality_rules": path_quality_rules,
            "exclusions_applied": len(data) != len(filtered_data) if data is not None else False,
            "original_rows": len(data) if data is not None else 0,
            "filtered_rows": len(filtered_data) if filtered_data is not None else 0
        }

        # ■■■■■■■■■■■■■ Analisis de nulos con configuración ■■■■■■■■■■■■■
        results["null_analysis"] = NullAnalyzer.count_nulls(filtered_data, path_quality_rules)

        # ■■■■■■■■■■■■■ Analisis de unicidad con configuración ■■■■■■■■■■■■■
        results["uniqueness_analysis"] = UniquenessAnalyzer.calculate_uniqueness(filtered_data, path_quality_rules)

        # ■■■■■■■■■■■■■ Analisis estadistico con configuración ■■■■■■■■■■■■■
        results["statistical_analysis"] = StatisticalAnalyzer.summary_stadistic(filtered_data, path_quality_rules)

        # ■■■■■■■■■■■■■ Informacion adicional de tipos con configuración ■■■■■■■■■■■■■
        results["count_types"] = StatisticalAnalyzer.count_by_type(filtered_data, path_quality_rules)

        # ■■■■■■■■■■■■■ Generar alertas basadas en configuración ■■■■■■■■■■■■■
        results["alerts"] = QualityAuditor.generate_alerts(filtered_data, path_quality_rules)

        return results

    @staticmethod
    def advance_quality_audit(
            data: RowDataType,
            path_quality_rules: Optional[str] = None,
            birth_column_name: Optional[str] = None,
            numerics_columns: Optional[list[str]] = None,
            text_columns: Optional[list[str]] = None
    ) -> dict[str, Any]:
        """
        Realiza un analisis completo de calidad de datos con opciones avanzadas usando configuración
        :param data: Lista de diccionarios representando filas de datos
        :param path_quality_rules: Ruta opcional al archivo YAML de configuración
        :param birth_column_name: Columna especifica para analisis de coherencia de fechas
        :param numerics_columns: Lista de columnas a tratar como nuemricas
        :param text_columns: Lista de columnas a tratar como de texto
        :return: Diccionario con todos los resultados de calidad ampliados
        """
        results = QualityAuditor.quality_audit(data, path_quality_rules)

        # ■■■■■■■■■■■■■ Cargar configuración para análisis avanzados ■■■■■■■■■■■■■
        config = QualityAuditor._load_configuration(path_quality_rules)
        filtered_data = QualityAuditor._apply_exclusions(data, config)
        all_rules = config.get('quality_rules', {}).get('data_type_rules', {})
        text_rules = all_rules.get('text', {})

        # ■■■■■■■■■■■■■ Analisis de fechas si se especifica una columna ■■■■■■■■■■■■■
        if birth_column_name is not None and birth_column_name.strip():
            date_result = DateAnalyzer.check_date_coherence(filtered_data, birth_column_name, path_quality_rules)
            results["date_analysis"] = dict()
            results["date_analysis"]["date_column"] = birth_column_name
            results["date_analysis"]["errors"] = date_result.get("errors", [])
            results["date_analysis"]["rules_applied"] = date_result.get("rules_applied", {})
            results["date_analysis"]["error_total"] = len(date_result.get("errors", []))

        # ■■■■■■■■■■■■■ Analisis estadistico detallado si se especifican columnas numericas ■■■■■■■■■■■■■
        if numerics_columns is not None and numerics_columns:
            numerics_values = StatisticalAnalyzer.get_numerics_values(filtered_data, path_quality_rules)
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
                for row in filtered_data:
                    if column in row.keys():
                        value = row[column]
                        if DataParser.is_string_value(value, text_rules):
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
        rows_total_count = len(data) if data is not None else 0

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
            path_quality_rules: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Genera alertas basadas en umbrales de calidad desde configuración
        :param data: Lista de diccionarios representando filas de datos
        :param path_quality_rules: Ruta opcional al archivo YAML de configuración
        :return: Diccionario con alertas y umbrales aplicados
        """
        alerts = list()
        if data is None or not data:
            return {"alerts": ["ALERTA: No hay datos para analizar"], "thresholds_applied": {}}

        # ■■■■■■■■■■■■■ Cargar umbrales desde configuración ■■■■■■■■■■■■■
        config = QualityAuditor._load_configuration(path_quality_rules)
        thresholds = QualityRulesReader.get_thresholds(config)

        # ■■■■■■■■■■■■■ Extraer umbrales para alertas ■■■■■■■■■■■■■
        warning_thresholds = thresholds.get('warning', {})
        critical_thresholds = thresholds.get('critical', {})

        thresholds_applied = {
            "null_percentage": {
                "warning": warning_thresholds.get('null_percentage', 25.0),
                "critical": critical_thresholds.get('null_percentage', 50.0)
            },
            "low_uniqueness": {
                "warning": warning_thresholds.get('low_uniqueness', 10.0),
                "critical": critical_thresholds.get('low_uniqueness', 5.0)
            },
            "high_uniqueness": {
                "warning": warning_thresholds.get('high_uniqueness', 90.0),
                "critical": critical_thresholds.get('high_uniqueness', 95.0)
            }
        }

        # ■■■■■■■■■■■■■ Aplicar exclusiones antes de análisis ■■■■■■■■■■■■■
        filtered_data = QualityAuditor._apply_exclusions(data, config)

        # ■■■■■■■■■■■■■ Analisis de nulos con umbrales configurados ■■■■■■■■■■■■■
        null_result = NullAnalyzer.count_nulls(filtered_data, path_quality_rules)
        count_nulls = null_result.get("null_counts", {})
        total_rows = len(filtered_data)

        for column in count_nulls.keys():
            nulls = count_nulls[column]
            percent_nulls = (nulls / total_rows) * 100.0

            # ▲▲▲▲▲▲ Determinar nivel de alerta para nulos ▲▲▲▲▲▲
            if percent_nulls >= critical_thresholds.get('null_percentage', 50.0):
                alert_level = "CRÍTICA"
            elif percent_nulls >= warning_thresholds.get('null_percentage', 25.0):
                alert_level = "ADVERTENCIA"
            else:
                continue

            message = f"""
                {alert_level}: Columna '{column}' tiene {round(percent_nulls, 2)}% de valores nulos
                (umbral crítica: {critical_thresholds.get('null_percentage', 50.0)}%, 
                umbral advertencia: {warning_thresholds.get('null_percentage', 25.0)}%)
                """
            alerts.append(message)

        # ■■■■■■■■■■■■■ Analisis de unicidad con umbrales configurados ■■■■■■■■■■■■■
        uniqueness_result = UniquenessAnalyzer.calculate_uniqueness(filtered_data, path_quality_rules)
        uniqueness = uniqueness_result.get("uniqueness_percentages", {})

        for column in uniqueness.keys():
            percent_uniqueness = uniqueness[column]

            # ▲▲▲▲▲ Determinar nivel de alerta para unicidad baja ▲▲▲▲▲
            if percent_uniqueness <= critical_thresholds.get('low_uniqueness', 5.0):
                alert_level = "CRÍTICA"
            elif percent_uniqueness <= warning_thresholds.get('low_uniqueness', 10.0):
                alert_level = "ADVERTENCIA"
            # ▲▲▲▲▲ Determinar nivel de alerta para unicidad alta ▲▲▲▲▲
            elif percent_uniqueness >= critical_thresholds.get('high_uniqueness', 95.0):
                alert_level = "INFO"
            elif percent_uniqueness >= warning_thresholds.get('high_uniqueness', 90.0):
                alert_level = "ADVERTENCIA"
            else:
                continue

            if percent_uniqueness <= warning_thresholds.get('low_uniqueness', 10.0):
                message = f"""
                {alert_level}: Columna '{column}' tiene baja unicidad: {round(percent_uniqueness, 2)}%
                (umbral crítica: {critical_thresholds.get('low_uniqueness', 5.0)}%, 
                umbral advertencia: {warning_thresholds.get('low_uniqueness', 10.0)}%)
                """
            else:
                message = f"""
                {alert_level}: Columna '{column}' tiene alta unicidad: {round(percent_uniqueness, 2)}%
                (umbral advertencia: {warning_thresholds.get('high_uniqueness', 90.0)}%, 
                umbral crítica: {critical_thresholds.get('high_uniqueness', 95.0)}%)
                """
            alerts.append(message)

        # ■■■■■■■■■■■■■ Alertas adicionales basadas en análisis estadístico ■■■■■■■■■■■■■
        statistical_result = StatisticalAnalyzer.summary_stadistic(filtered_data, path_quality_rules)
        out_of_range = statistical_result.get("out_of_range", {})

        for column, violations in out_of_range.items():
            if violations:
                alert_level = "CRÍTICA" if len(violations) > 5 else "ADVERTENCIA"
                message = f"""
                {alert_level}: Columna '{column}' tiene {len(violations)} valores fuera de rango
                """
                alerts.append(message)

        return {
            "alerts": alerts,
            "thresholds_applied": thresholds_applied,
            "total_alerts": len(alerts),
            "critical_alerts": len([a for a in alerts if "CRÍTICA" in a]),
            "warning_alerts": len([a for a in alerts if "ADVERTENCIA" in a]),
            "info_alerts": len([a for a in alerts if "INFO" in a])
        }

    # ■■■■■■■■■■■■■ Funciones helper para manejo de configuración ■■■■■■■■■■■■■

    @staticmethod
    def _load_configuration(path_quality_rules: Optional[str]) -> dict[str, Any]:
        """
        Carga configuración desde archivo YAML o usa valores por defecto
        :param path_quality_rules: Ruta opcional al archivo YAML de configuración
        :return: Diccionario con configuración cargada
        """
        if path_quality_rules:
            try:
                return QualityRulesReader.load_configs(path_quality_rules)
            except (FileNotFoundError, ValueError, Exception):
                # ■■■■■■■■■■■■■ Si hay error, usar valores por defecto ■■■■■■■■■■■■■
                pass

        # ■■■■■■■■■■■■■ Valores por defecto si no hay configuración ■■■■■■■■■■■■■
        return QualityRulesReader.apply_default_rules()

    @staticmethod
    def _apply_exclusions(data: RowDataType, config: dict[str, Any]) -> RowDataType:
        """
        Aplica reglas de exclusión desde configuración
        :param data: Lista de diccionarios representando filas de datos
        :param config: Configuración cargada
        :return: Datos filtrados según exclusiones
        """
        exclusion_rules = config.get('quality_rules', {}).get('exclusion_rules', {})

        if not exclusion_rules:
            return data

        # ■■■■■■■■■■■■■ Obtener columnas y valores a excluir ■■■■■■■■■■■■■
        exclude_columns = exclusion_rules.get('exclude_columns', [])
        exclude_values = exclusion_rules.get('exclude_values', {})

        if not exclude_columns and not exclude_values:
            return data

        if data is None or not data:
            return data
        
        filtered_data = list()

        for row in data:
            should_exclude = False

            # ▲▲▲▲▲▲ Verificar si la fila debe excluirse por valores específicos ▲▲▲▲▲▲
            for column, values_to_exclude in exclude_values.items():
                if column in row and row[column] in values_to_exclude:
                    should_exclude = True
                    break

            # ▲▲▲▲▲▲ Verificar si la fila contiene columnas excluidas ▲▲▲▲▲▲
            if not should_exclude and exclude_columns:
                for column in exclude_columns:
                    if column in row:
                        should_exclude = True
                        break

            if not should_exclude:
                filtered_data.append(row)

        return filtered_data
