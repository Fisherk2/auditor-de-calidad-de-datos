"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Generación de informes estructurados
AUTOR:       Fisherk2
FECHA:       2026-02-19
DESCRIPCIÓN: Proporciona funciones para generar informes legibles y estructurados
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""
from typing import Dict, Any, Optional
from datetime import datetime
import json
import os

from quality_auditor.main_auditor import QualityAuditor

# ⋮⋮⋮⋮⋮⋮⋮⋮ ALIAS de estructura datos ⋮⋮⋮⋮⋮⋮⋮⋮
RowDataType = list[dict[str, Any]]


class QualityReport:
    """
    Clase para generar informes estructurados de calidad de datos
    """

    @staticmethod
    def generate_json_report(results: dict[str, Any]) -> str:
        """
        Genera un informe en formato JSON
        :param results: Diccionario con resultados de analisis de validacion y calidad
        :return: String con formato JSON del informe
        """
        try:
            json_raw: str = json.dumps(results, indent=2, ensure_ascii=False)
            return json_raw
        except Exception as e:
            return f"Error al generar el informe JSON: {str(e)}"

    @staticmethod
    def generate_report(data: RowDataType, path_quality_rules: Optional[str] = None) -> dict[str, Any]:
        """
        Genera un informe completo basado en configuración usando el QualityAuditor
        :param data: Lista de diccionarios representando filas de datos
        :param path_quality_rules: Ruta opcional al archivo YAML de configuración
        :return: Diccionario con resultados completos del análisis
        """
        return QualityAuditor.quality_audit(data, path_quality_rules)

    @staticmethod
    def generate_alerts_report(data: RowDataType, path_quality_rules: Optional[str] = None) -> dict[str, Any]:
        """
        Genera específicamente un informe de alertas basado en umbrales de configuración
        :param data: Lista de diccionarios representando filas de datos
        :param path_quality_rules: Ruta opcional al archivo YAML de configuración
        :return: Diccionario con alertas y umbrales aplicados
        """
        return QualityAuditor.generate_alerts(data, path_quality_rules)

    @staticmethod
    def generate_summary_report(results: dict[str, Any]) -> str:
        """
        Genera un informe resumido en formato texto
        :param results: Diccionario con resultados de analisis de validacion y calidad
        :return: String con formato de texto del informe resumido
        """
        report = list()
        report.append(
            "🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙 INFORME DE CALIDAD DE DATOS 🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙")
        report.append("")

        if "timestamp" in results.keys():
            report.append(f"Fecha y hora del análisis: {results["timestamp"]}")
            report.append("")
        if "total_rows" in results.keys():
            report.append(f"Total de filas analizadas: {str(results["total_rows"])}")
            report.append("")

        # ■■■■■■■■■■■■■ Metricas generales si estan disponibles ■■■■■■■■■■■■■
        if "general_metrics" in results.keys():
            metrics = results["general_metrics"]
            report.append("▏▎▍▌▋▊▉▉▉▉▉▉▉▉ MÉTRICAS GENERALES ▉▉▉▉▉▉▉▉▉▊▋▌▍▎")
            report.append("")
            report.append(f"Calidad general de los datos: {str(metrics['general_quality'])}%")
            report.append(f"Porcentaje de datos nulos: {str(metrics['nulls_percent'])}%")
            report.append(f"Promedio de unicidad: {str(metrics['average_uniqueness'])}%")
            report.append("")

        # ■■■■■■■■■■■■■ Analisis de nulos (compatible con ambos formatos) ■■■■■■■■■■■■■
        if "null_analysis" in results.keys():
            nulls = results["null_analysis"]
            report.append("▏▎▍▌▋▊▉▉▉▉▉▉▉▉ ANÁLISIS DE NULOS ▉▉▉▉▉▉▉▉▉▊▋▌▍▎")

            # ▲▲▲▲▲▲ Manejar formato antiguo (directo) ▲▲▲▲▲▲
            if isinstance(nulls, dict) and any(isinstance(v, int) for v in nulls.values()):
                for column in nulls.keys():
                    count = nulls[column]
                    if count > 0:
                        report.append(f"    {column}: {count} valores nulos")
                if not nulls or not any(nulls.values()):
                    report.append("    No se encontraron valores nulos")

            # ▲▲▲▲▲▲ Manejar nuevo formato (con reglas) ▲▲▲▲▲▲
            elif isinstance(nulls, dict) and "null_counts" in nulls:
                null_counts = nulls["null_counts"]
                rules_applied = nulls.get("rules_applied", {})
                for column in null_counts.keys():
                    count = null_counts[column]
                    if count > 0:
                        report.append(f"    {column}: {count} valores nulos")
                if not null_counts or not any(null_counts.values()):
                    report.append("    No se encontraron valores nulos")
                if rules_applied:
                    report.append(f"    Reglas aplicadas: {rules_applied}")
            report.append("")

        # ■■■■■■■■■■■■■ Analisis de unicidad (compatible con ambos formatos) ■■■■■■■■■■■■■
        if "uniqueness_analysis" in results.keys():
            uniqueness = results["uniqueness_analysis"]
            report.append("▏▎▍▌▋▊▉▉▉▉▉▉▉▉ ANÁLISIS DE UNICIDAD ▉▉▉▉▉▉▉▉▉▊▋▌▍▎")

            # ▲▲▲▲▲▲ Manejar formato antiguo (directo) ▲▲▲▲▲▲
            if isinstance(uniqueness, dict) and any(isinstance(v, (int, float)) for v in uniqueness.values()):
                for column in uniqueness.keys():
                    percent = uniqueness[column]
                    report.append(f"    {column}: {percent}% unicos")

            # ▲▲▲▲▲▲ Manejar nuevo formato (con reglas) ▲▲▲▲▲▲
            elif isinstance(uniqueness, dict) and "uniqueness_percentages" in uniqueness:
                uniqueness_percentages = uniqueness["uniqueness_percentages"]
                rules_applied = uniqueness.get("rules_applied", {})
                for column in uniqueness_percentages.keys():
                    percent = uniqueness_percentages[column]
                    report.append(f"    {column}: {percent}% unicos")
                if rules_applied:
                    report.append(f"    Reglas aplicadas: {rules_applied}")
            report.append("")

        # ■■■■■■■■■■■■■ Analisis estadistico (compatible con ambos formatos) ■■■■■■■■■■■■■
        if "statistical_analysis" in results.keys():
            statistical = results["statistical_analysis"]
            if statistical:
                report.append("▏▎▍▌▋▊▉▉▉▉▉▉▉▉ ANÁLISIS ESTADÍSTICO ▉▉▉▉▉▉▉▉▉▊▋▌▍▎")

                # ▲▲▲▲▲▲ Manejar formato antiguo ▲▲▲▲▲▲
                if isinstance(statistical, dict) and any(
                        isinstance(v, dict) and "minimum" in v for v in statistical.values()):
                    for column in statistical.keys():
                        metrics = statistical[column]
                        report.append(f"▲▲▲▲▲▲ Columna {column} ▲▲▲▲▲▲")
                        report.append(f"    Mínimo: {metrics.get('minimum', 'N/A')}")
                        report.append(f"    Máximo: {metrics.get('maximum', 'N/A')}")
                        report.append(f"    Promedio: {metrics.get('average', 'N/A')}")
                        report.append(f"    Conteo: {metrics.get('count', 'N/A')}")
                        report.append("")

                # ▲▲▲▲▲▲ Manejar nuevo formato (con statistics y out_of_range) ▲▲▲▲▲▲
                elif isinstance(statistical, dict) and "statistics" in statistical:
                    stats = statistical["statistics"]
                    out_of_range = statistical.get("out_of_range", {})
                    rules_applied = statistical.get("rules_applied", {})

                    for column in stats.keys():
                        metrics = stats[column]
                        report.append(f"▲▲▲▲▲▲ Columna {column} ▲▲▲▲▲▲")
                        report.append(f"    Mínimo: {metrics.get('minimum', 'N/A')}")
                        report.append(f"    Máximo: {metrics.get('maximum', 'N/A')}")
                        report.append(f"    Promedio: {metrics.get('average', 'N/A')}")
                        report.append(f"    Conteo: {metrics.get('count', 'N/A')}")
                        report.append(f"    Desviación estándar: {metrics.get('standard_deviation', 'N/A')}")

                        # ▲▲▲▲▲▲ Mostrar valores fuera de rango si existen ▲▲▲▲▲▲
                        if column in out_of_range and out_of_range[column]:
                            violations = out_of_range[column]
                            report.append(f"    Valores fuera de rango: {len(violations)}")
                            for violation in violations[:3]:  # Mostrar solo primeros 3
                                report.append(
                                    f"      - Fila {violation['row_index']}: {violation['value']} ({violation['reason']})")
                            if len(violations) > 3:
                                report.append(f"      ... y {len(violations) - 3} más")
                        report.append("")

                    if rules_applied:
                        report.append(f"Reglas aplicadas: {rules_applied}")
                        report.append("")

        return "\n".join(report)

    @staticmethod
    def generate_detail_report(results: dict[str, Any]) -> str:
        """
        Genera un informe detallado en formato texto
        :param results: Diccionario con resultados de analisis de calidad
        :return: String con formato de texto del informe detallado
        """
        report = list()
        report.append(
            "🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙 INFORME DETALLADO DE CALIDAD DE DATOS 🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙")
        report.append("▢▣" * 20)
        report.append("")

        # ■■■■■■■■■■■■■ Informacion general ■■■■■■■■■■■■■
        if "timestamp" in results.keys():
            report.append(f"Timestamp del analisis: {results["timestamp"]}")
        if "total_rows" in results.keys():
            report.append(f"Numero todal de filas: {results["total_rows"]}")

        report.append("")

        # ■■■■■■■■■■■■■ Incluir todos los analisis disponibles ■■■■■■■■■■■■■
        seccions = dict()
        seccions["NULL_ANALYSIS"] = "null_analysis"
        seccions["UNIQUENESS_ANALYSIS"] = "uniqueness_analysis"
        seccions["STATISTICAL_ANALYSIS"] = "statistical_analysis"
        seccions["DATE_ANALYSIS"] = "date_analysis"
        seccions["STATISTICAL_DETAILS"] = "statistical_details"
        seccions["COUNT_TYPES"] = "count_types"
        for title in seccions.keys():
            key = seccions[title]
            if key in results.keys():
                data = results[key]
                report.append(f"▏▎▍▌▋▊▉▉▉▉▉▉▉▉ {title} ▉▉▉▉▉▉▉▉▉▊▋▌▍▎")
                if isinstance(data, dict):
                    for key in data.keys():
                        value = data[key]
                        if isinstance(value, Dict):
                            report.append(f"■■■■■■■■■■■■■ {key} ■■■■■■■■■■■■■")
                            for subkey in value.keys():
                                report.append(f"    {subkey}: {str(value[subkey])}")
                        else:
                            report.append(f"    {key}: {str(value)}")
                else:
                    report.append(f"    {str(data)}")
                report.append("")

        # ■■■■■■■■■■■■■ Alertas si están disponibles ■■■■■■■■■■■■■
        if "alerts" in results.keys():
            alerts = results["alerts"]
            if alerts:
                report.append(
                    "🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙 ALERTAS IMPORTANTES 🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙")
                for alert in alerts:
                    report.append(f"# ⋮⋮⋮⋮⋮⋮⋮⋮ {alert} ⋮⋮⋮⋮⋮⋮⋮⋮ ")
                report.append("")

        report.append("▢▣" * 20)
        report.append("■■■■■■■■■■■■■ Fin del informe ■■■■■■■■■■■■■ ")

        return "\n".join(report)

    @staticmethod
    def save_report(results: dict[str, Any], path_file: str, format_file: str = "json"):
        """
        Guarda el informe en un archivo
        :param results: Diccionario con resultados de analisis de calidad
        :param path_file: Ruta donde guardar el archivo
        :param format_file: Formato del informe ("json","summary,"detailed")
        :return:
        """
        content = ""
        if format_file.lower() == "json":
            content = QualityReport.generate_json_report(results)
        elif format_file.lower() == "summary":
            content = QualityReport.generate_summary_report(results)
        elif format_file.lower() == "detailed":
            content = QualityReport.generate_detail_report(results)

        # ■■■■■■■■■■■■■ Default a JSON ■■■■■■■■■■■■■
        else:
            content = QualityReport.generate_json_report(results)

        try:
            with open(path_file, 'w', encoding='utf-8') as file:
                file.write(content)
        except IOError as e:
            print(f"Error al guardar el informe: {e}")

    @staticmethod
    def consolidate_results(result_list: RowDataType) -> dict[str, Any]:
        """
        Consolida multiples resultados de analisis en uno solo
        :param result_list: Lista de diccionarios con resultados de analisis
        :return: Diccionario consolidado con todoslos resultados
        """
        if result_list is None or not result_list:
            return dict()
        consolidate_result = dict()
        consolidate_result["timestamp"] = datetime.now().isoformat()
        consolidate_result["total_analysis"] = len(result_list)
        consolidate_result["individual_results"] = result_list

        # ■■■■■■■■■■■■■ Consolidar analisis de nulos ■■■■■■■■■■■■■
        nulls_consolidate = dict()
        for result in result_list:
            if "null_analysis" in result.keys():
                nulls = result["null_analysis"]

                # ▲▲▲▲▲▲ Manejar formato antiguo (directo) ▲▲▲▲▲▲
                if isinstance(nulls, dict) and any(isinstance(v, int) for v in nulls.values()):
                    for column in nulls.keys():
                        if not column in nulls_consolidate.keys():
                            nulls_consolidate[column] = 0
                        nulls_consolidate[column] += nulls[column]

                # ▲▲▲▲▲▲ Manejar nuevo formato (con null_counts) ▲▲▲▲▲▲
                elif isinstance(nulls, dict) and "null_counts" in nulls:
                    null_counts = nulls["null_counts"]
                    for column in null_counts.keys():
                        if not column in nulls_consolidate.keys():
                            nulls_consolidate[column] = 0
                        nulls_consolidate[column] += null_counts[column]

        consolidate_result["nulls_analysis_consolidate"] = nulls_consolidate

        # ■■■■■■■■■■■■■ Consolidar analisis de unicidad (promedio) ■■■■■■■■■■■■■
        uniqueness_consolidate = dict()
        uniqueness_count = dict()
        for result in result_list:
            if "uniqueness_analysis" in result.keys():
                uniqueness = result["uniqueness_analysis"]

                # ▲▲▲▲▲▲ Manejar formato antiguo (directo) ▲▲▲▲▲▲
                if isinstance(uniqueness, dict) and any(isinstance(v, (int, float)) for v in uniqueness.values()):
                    for column in uniqueness.keys():
                        if not column in uniqueness_consolidate.keys():
                            uniqueness_consolidate[column] = 0
                            uniqueness_count[column] = 0
                        uniqueness_consolidate[column] += uniqueness[column]
                        uniqueness_count[column] += 1

                # ▲▲▲▲▲▲ Manejar nuevo formato (con uniqueness_percentages) ▲▲▲▲▲▲
                elif isinstance(uniqueness, dict) and "uniqueness_percentages" in uniqueness:
                    uniqueness_percentages = uniqueness["uniqueness_percentages"]
                    for column in uniqueness_percentages.keys():
                        if not column in uniqueness_consolidate.keys():
                            uniqueness_consolidate[column] = 0
                            uniqueness_count[column] = 0
                        uniqueness_consolidate[column] += uniqueness_percentages[column]
                        uniqueness_count[column] += 1

        # ■■■■■■■■■■■■■ Calcular promedios ■■■■■■■■■■■■■
        for column in uniqueness_consolidate.keys():
            if column in uniqueness_count.keys() and uniqueness_count[column] > 0:
                uniqueness_consolidate[column] = uniqueness_consolidate[column] / uniqueness_count[column]

        consolidate_result["uniqueness_analysis_consolidate"] = uniqueness_consolidate

        return consolidate_result

    @staticmethod
    def save_report_with_timestamp(results: dict[str, Any], base_path: str = "data/output/quality_report",
                                   format_file: str = "json") -> str:
        """
        Guarda el informe agregando timestamp automático al nombre del archivo
        :param results: Diccionario con resultados de análisis de calidad
        :param base_path: Ruta base sin extensión (ej: "data/output/quality_report")
        :param format_file: Formato del informe ("json", "summary", "detailed")
        :return: Ruta completa del archivo guardado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        extension = "json" if format_file.lower() == "json" else "txt"

        # ▲▲▲▲▲▲ Asegurar que la ruta base no tenga extensión ▲▲▲▲▲▲
        if base_path.endswith('.json') or base_path.endswith('.txt'):
            base_path = base_path.rsplit('.', 1)[0]

        full_path = f"{base_path}_{timestamp}.{extension}"

        # ▲▲▲▲▲▲ Crear directorio si no existe ▲▲▲▲▲▲
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        QualityReport.save_report(results, full_path, format_file)
        return full_path

    @staticmethod
    def generate_error_report(error_list: list[str], file_path: str = "data/output/quality_error_report.txt") -> bool:
        """
        Genera un archivo de texto plano con lista de errores o mensajes
        :param error_list: Lista de mensajes de error
        :param file_path: Ruta donde guardar el archivo de errores
        :return: True si se guardó exitosamente, False en caso contrario
        """
        try:
            # ▲▲▲▲▲▲ Crear directorio si no existe ▲▲▲▲▲▲
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(
                    "🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙 REPORTE DE ERRORES 🮙🮘🮙🮙🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙\n")
                file.write(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write(f"Total de errores: {len(error_list)}\n")
                file.write("▢▣" * 30 + "\n\n")

                for i, error in enumerate(error_list, 1):
                    file.write(f"{i}. {error}\n")

                file.write("\n" + "▢▣" * 30 + "\n")
                file.write("■■■■■■■■■■■■■ Fin del reporte de errores ■■■■■■■■■■■■■\n")

            return True
        except IOError as e:
            print(f"Error al guardar reporte de errores: {e}")
            return False
