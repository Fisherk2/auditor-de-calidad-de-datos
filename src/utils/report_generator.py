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
    def generate_JSON_report(results:dict[str, Any]) -> str:
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

            informe.append("")

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



# ▼△▼△▼△▼△▼△▼△▼△▼△▼△ Pseudocodigo △▼△▼△▼△▼△▼△▼△▼△▼△▼

public
static
String
generarInformeDetallado(Dict[String, Any]
resultados)
"""
Genera un informe detallado en formato texto

Args:
    resultados: Diccionario con resultados de análisis de calidad

Returns:
    String con formato de texto del informe detallado
"""
var
informe = list()
informe.append("=== INFORME DETALLADO DE CALIDAD DE DATOS ===")
informe.append("=" * 50)
informe.append("")

# Información general
if resultados.containsKey("timestamp")
    informe.append("Timestamp del análisis: " + resultados["timestamp"])

if resultados.containsKey("total_filas")
    informe.append("Número total de filas: " + str(resultados["total_filas"]))

informe.append("")

# Incluir todos los análisis disponibles
var
secciones = dict()
secciones["ANÁLISIS DE NULOS"] = "analisis_nulos"
secciones["ANÁLISIS DE UNICIDAD"] = "analisis_unicidad"
secciones["ANÁLISIS ESTADÍSTICO"] = "analisis_estadistico"
secciones["ANÁLISIS DE FECHAS"] = "analisis_fechas"
secciones["ESTADÍSTICOS DETALLES"] = "estadisticos_detalles"
secciones["CONTEO POR TIPO"] = "conteo_tipos"

for String titulo in secciones.keySet()
    var
    clave = secciones[titulo]
    if resultados.containsKey(clave)
        var
        datos = resultados[clave]
        informe.append("--- " + titulo + " ---")

        if isinstance(datos, Dict)
            for String key in datos.keySet()
                var
                value = datos[key]
                if isinstance(value, Dict)
                    informe.append("  " + key + ":")
                    for String subkey in value.keySet()
                        informe.append("    " + subkey + ": " + str(value[subkey]))
                else
                    informe.append("  " + key + ": " + str(value))
        else
            informe.append("  " + str(datos))

        informe.append("")

# Agregar alertas si están disponibles
if resultados.containsKey("alertas")
    var
    alertas = resultados["alertas"]
    if !alertas.isEmpty()
    informe.append("--- ALERTAS IMPORTANTES ---")
    for String alerta in alertas
        informe.append("! " + alerta)
    informe.append("")

informe.append("=" * 50)
informe.append("Fin del informe")

return "\n".join(informe)

public
static
void
guardarInforme(Dict[String, Any]
resultados, String
rutaArchivo, String
formato = "json")
"""
Guarda el informe en un archivo

Args:
    resultados: Diccionario con resultados de análisis de calidad
    rutaArchivo: Ruta donde guardar el archivo
    formato: Formato del informe ("json", "resumen", "detallado")
"""
var
contenido = ""

if formato.toLowerCase() == "json"
    contenido = ReportGenerator.generarInformeJSON(resultados)
else if formato.toLowerCase() == "resumen"
contenido = ReportGenerator.generarInformeResumen(resultados)
else if formato.toLowerCase() == "detallado"
    contenido = ReportGenerator.generarInformeDetallado(resultados)
else
    contenido = ReportGenerator.generarInformeJSON(resultados)  # Default to JSON

try
    with open(rutaArchivo, 'w', encoding='utf-8') as file
        file.write(contenido)
catch
IOError
e
print("Error al guardar el informe: " + str(e))

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