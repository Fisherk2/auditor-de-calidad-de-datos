"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Generación de informes estructurados
AUTOR:       Fisherk2
FECHA:       2026-02-18
DESCRIPCIÓN: Proporciona funciones para generar informes legibles y estructurados
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""
from typing import Dict, Any, List
from datetime import datetime
import json

# ⋮⋮⋮⋮⋮⋮⋮⋮ ALIAS de estructura datos ⋮⋮⋮⋮⋮⋮⋮⋮
RowDataType = list[dict[str, Any]]
MetricDataType = dict[str, dict[str, float]]
ValueListType = dict[str, list[float]]

class ReportGenerator:
    """
    Clase para generar informes estructurados de calidad de datos
    """

    @staticmethod
    def generate_json_report(results:dict[str, Any]) -> str:
        """
        Genera un informe en formato JSON
        :param results: Diccionario con resultados de analisis de validacion y calidad
        :return: String con formato JSON del informe
        """
        try:
            json_raw:str = json.dumps(results, indent=2, ensure_ascii=False)
            return json_raw
        except Exception as e: # TODO: Colocar as en toda las excepciones del proyecto
            return f"Error al generar el informe JSON: {str(e)}"

    @staticmethod
    def generate_summary_report(results:dict[str, Any]) -> str:
        """
        Genera un informe resumido en formato texto
        :param results: Diccionario con resultados de analisis de validacion y calidad
        :return: String con formato de texto del informe resumido
        """
        report = list()
        report.append("🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙 INFORME DE CALIDAD DE DATOS 🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙")
        report.append("")

        if "timestamp" in results.keys():
            report.append(f"Fecha y hora del análisis: {results["timestamp"]}")
            report.append("")
        if "total_rows" in results.keys():
            report.append(f"Total de filas analizadas: {str(results["total_rows"])}")
            report.append("")

        # TODO: Investigar llave su nombre correcto ■■■■■■■■■■■■■ Metricas generales si estan disponibles ■■■■■■■■■■■■■
        if "general_metrics" in results.keys():
            metrics = results["general_metrics"]
            report.append("▏▎▍▌▋▊▉▉▉▉▉▉▉▉ MÉTRICAS GENERALES ▉▉▉▉▉▉▉▉▉▊▋▌▍▎")
            report.append("")
            report.append(f"Calidad general de los datos: {str(metrics["general_quality"])}%")
            report.append(f"Porcentaje de datos nulos: {str(metrics["nulls_percent"])}%")
            report.append(f"Promedio de unicidad: {str(metrics["average_uniqueness"])}%")
            report.append("")

        # TODO: Investigar llave su nombre correcto ■■■■■■■■■■■■■ Analisis de nulos ■■■■■■■■■■■■■
        if "null_analysis" in results.keys():
            nulls = results["null_analysis"]
            report.append("▏▎▍▌▋▊▉▉▉▉▉▉▉▉ ANÁLISIS DE NULOS ▉▉▉▉▉▉▉▉▉▊▋▌▍▎")
            for column in nulls.keys():
                count = nulls[column]
                if count > 0:
                    report.append(f"    {column}: {count} valores nulos")
            if not nulls or report[len(report)-1] != "▏▎▍▌▋▊▉▉▉▉▉▉▉▉ ANÁLISIS DE NULOS ▉▉▉▉▉▉▉▉▉▊▋▌▍▎":
                report.append(f"    No se encontraron valores nulos")
            report.append("")

        # TODO: Investigar llave su nombre correcto ■■■■■■■■■■■■■ Analisis de unicidad ■■■■■■■■■■■■■
        if "uniqueness_analysis" in results.keys():
            uniqueness = results["uniqueness_analysis"]
            report.append("▏▎▍▌▋▊▉▉▉▉▉▉▉▉ ANÁLISIS DE UNICIDAD ▉▉▉▉▉▉▉▉▉▊▋▌▍▎")
            for column in uniqueness.keys():
                percent = uniqueness[column]
                report.append(f"    {column}: {percent}% unicos")

            report.append("")

        # TODO: Investigar llave su nombre correcto ■■■■■■■■■■■■■ Analisis de estadístico ■■■■■■■■■■■■■
        if "statistical_analysis" in results.keys():
            statistical = results["statistical_analysis"]
            if statistical:
                report.append("▏▎▍▌▋▊▉▉▉▉▉▉▉▉ ANÁLISIS DE ESTADÍSTICO ▉▉▉▉▉▉▉▉▉▊▋▌▍▎")
                for column in statistical.keys():
                    metrics = statistical[column]
                    report.append(f"▲▲▲▲▲▲ Columna {column} ▲▲▲▲▲▲")
                    report.append(f"    Minimo: {metrics.get('minimum', "N/A")}")
                    report.append(f"    Maximo: {metrics.get('maximum', "N/A")}")
                    report.append(f"    Promedio: {metrics.get('average', "N/A")}")
                    report.append(f"    Conteo: {metrics.get('count', "N/A")}")
                    report.append("")

        return "\n".join(report)

    @staticmethod
    def generate_detail_report(results: dict[str, Any] ) -> str:
        """
        Genera un informe detallado en formato texto
        :param results: Diccionario con resultados de analisis de calidad
        :return: String con formato de texto del informe detallado
        """
        report = list()
        report.append("🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙 INFORME DETALLADO DE CALIDAD DE DATOS 🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙")
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
        seccions["DATE_ANALYSIS"]= "date_analysis"
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
                        if isinstance(value,Dict):
                            report.append(f"■■■■■■■■■■■■■ {key} ■■■■■■■■■■■■■" )
                            for subkey in value.keys():
                                report.append(f"    {subkey}: {str(value[subkey])}")
                        else:
                            report.append(f"    {key}: {str(value)}")
                else:
                    report.append(f"    {str(data)}")
                report.append("")

        # TODO: Investigar llave su nombre correcto ■■■■■■■■■■■■■ Agregar alertas si están disponibles ■■■■■■■■■■■■■
        if "alerts" in results.keys():
            alerts = results["alerts"]
            if alerts:
                report.append("🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙 ALERTAS IMPORTANTES 🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙🮙🮘🮙🮘🮙")
                for alert in alerts:
                    report.append(f"# ⋮⋮⋮⋮⋮⋮⋮⋮ {alert} ⋮⋮⋮⋮⋮⋮⋮⋮ ")
                report.append("")

        report.append("▢▣" * 20)
        report.append("■■■■■■■■■■■■■ Fin del informe ■■■■■■■■■■■■■ ")

        return "\n".join(report)

    @staticmethod
    def save_report(results:dict[str,Any], path_file:str, format_file:str= "json"):
        """
        Guarda el informe en un archivo
        :param results: Diccionario con resultados de analisis de calidad
        :param path_file: Ruta donde guardar el archivo
        :param format_file: Formato del informe ("json","summary,"detailed")
        :return:
        """
        content = ""
        if format_file.lower()== "json":
            content = ReportGenerator.generate_json_report(results)
        elif format_file.lower()== "summary":
            content = ReportGenerator.generate_summary_report(results)
        elif format_file.lower()== "detailed":
            content = ReportGenerator.generate_detail_report(results)

        # ■■■■■■■■■■■■■ Default to JSON ■■■■■■■■■■■■■
        else:
            content = ReportGenerator.generate_json_report(results)

        try:
            with open(path_file,'w',encoding='utf-8') as file:
                file.write(content)
        except IOError as e:
            print(f"Error al guardar el informe: {e}")
# ▼△▼△▼△▼△▼△▼△▼△▼△▼△ Pseudocodigo △▼△▼△▼△▼△▼△▼△▼△▼△▼

public
static
Dict[String, Any]
consolidarResultados(List[Dict[String, Any]]
listaResultados)
"""
Consolida múltiples resultados de análisis en uno solo

Args:
    listaResultados: Lista de diccionarios con resultados de análisis

Returns:
    Diccionario consolidado con todos los resultados
"""
if listaResultados == null | | listaResultados.isEmpty()
    return dict()

var
resultadoConsolidado = dict()
resultadoConsolidado["timestamp"] = datetime.now().isoformat()
resultadoConsolidado["total_analisis"] = listaResultados.size()
resultadoConsolidado["resultados_individuales"] = listaResultados

# Consolidar análisis de nulos
var
consolidadoNulos = dict()
for Dict[String, Any] resultado in listaResultados
    if resultado.containsKey("analisis_nulos")
        var
        nulos = resultado["analisis_nulos"]
        for String columna in nulos.keySet()
            if !consolidadoNulos.containsKey(columna)
            consolidadoNulos[columna] = 0
        consolidadoNulos[columna] += nulos[columna]

resultadoConsolidado["analisis_nulos_consolidado"] = consolidadoNulos

# Consolidar análisis de unicidad (promedio)
var
consolidadoUnicidad = dict()
var
conteoUnicidad = dict()

for Dict[String, Any] resultado in listaResultados
    if resultado.containsKey("analisis_unicidad")
        var
        unicidad = resultado["analisis_unicidad"]
        for String columna in unicidad.keySet()
            if !consolidadoUnicidad.containsKey(columna)
            consolidadoUnicidad[columna] = 0.0
            conteoUnicidad[columna] = 0

        consolidadoUnicidad[columna] += unicidad[columna]
        conteoUnicidad[columna] + +

# Calcular promedios
for String columna in consolidadoUnicidad.keySet()
    if conteoUnicidad.containsKey(columna) & & conteoUnicidad[columna] > 0
        consolidadoUnicidad[columna] = consolidadoUnicidad[columna] / conteoUnicidad[columna]

resultadoConsolidado["analisis_unicidad_consolidado"] = consolidadoUnicidad

return resultadoConsolidado