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


# ▼△▼△▼△▼△▼△▼△▼△▼△▼△ Pseudocodigo △▼△▼△▼△▼△▼△▼△▼△▼△▼

public
static
String
generarInformeResumen(Dict[String, Any]
resultados)
"""
Genera un informe resumido en formato texto

Args:
    resultados: Diccionario con resultados de análisis de calidad

Returns:
    String con formato de texto del informe resumido
"""
var
informe = list()
informe.append("=== INFORME DE CALIDAD DE DATOS ===")
informe.append("")

if resultados.containsKey("timestamp")
    informe.append("Fecha y hora del análisis: " + resultados["timestamp"])
    informe.append("")

if resultados.containsKey("total_filas")
    informe.append("Total de filas analizadas: " + str(resultados["total_filas"]))
    informe.append("")

# Métricas generales si están disponibles
if resultados.containsKey("metricas_generales")
    var
    metricas = resultados["metricas_generales"]
    informe.append("--- MÉTRICAS GENERALES ---")

    if metricas.containsKey("calidad_general")
        informe.append("Calidad general de los datos: " + str(metricas["calidad_general"]) + "%")

    if metricas.containsKey("porcentaje_datos_nulos")
        informe.append("Porcentaje de datos nulos: " + str(metricas["porcentaje_datos_nulos"]) + "%")

    if metricas.containsKey("promedio_unicidad")
        informe.append("Promedio de unicidad: " + str(metricas["promedio_unicidad"]) + "%")

    informe.append("")

# Análisis de nulos
if resultados.containsKey("analisis_nulos")
    var
    nulos = resultados["analisis_nulos"]
    informe.append("--- ANÁLISIS DE NULOS ---")

    for String columna in nulos.keySet()
        var
        conteo = nulos[columna]
        if conteo > 0
            informe.append("  " + columna + ": " + str(conteo) + " valores nulos")

    if nulos.isEmpty() | | informe[informe.size() - 1] != "--- ANÁLISIS DE NULOS ---"
        informe.append("  No se encontraron valores nulos")

    informe.append("")

# Análisis de unicidad
if resultados.containsKey("analisis_unicidad")
    var
    unicidad = resultados["analisis_unicidad"]
    informe.append("--- ANÁLISIS DE UNICIDAD ---")

    for String columna in unicidad.keySet()
        var
        porcentaje = unicidad[columna]
        informe.append("  " + columna + ": " + str(porcentaje) + "% únicos")

    informe.append("")

# Análisis estadístico
if resultados.containsKey("analisis_estadistico")
    var
    estadisticos = resultados["analisis_estadistico"]
    if !estadisticos.isEmpty()
    informe.append("--- ANÁLISIS ESTADÍSTICO ---")

    for String columna in estadisticos.keySet()
        var
        metrics = estadisticos[columna]
        informe.append("  Columna: " + columna)
        informe.append("    Mínimo: " + str(metrics.get("min", "N/A")))
        informe.append("    Máximo: " + str(metrics.get("max", "N/A")))
        informe.append("    Promedio: " + str(metrics.get("promedio", "N/A")))
        informe.append("    Conteo: " + str(metrics.get("conteo", "N/A")))
        informe.append("")

return "\n".join(informe)

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