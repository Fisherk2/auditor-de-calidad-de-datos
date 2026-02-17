"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Coordinador de todos los analisis de calidad de datos
AUTOR:       Fisherk2
FECHA:       2026-02-17
DESCRIPCIÓN: Proporciona un punto de entrada centralizado para todas las funciones de auditoría (Patrón Strategy)
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""
from typing import Any, Optional
from datetime import datetime

from src.quality_auditor.null_analyzer import NullAnalyzer
from src.quality_auditor.uniqueness_analyzer import UniquenessAnalyzer
from src.quality_auditor.date_analyzer import DateAnalyzer
from src.quality_auditor.statistical_analyzer import StatisticalAnalyzer

# ⋮⋮⋮⋮⋮⋮⋮⋮ ALIAS de estructura datos ⋮⋮⋮⋮⋮⋮⋮⋮
RowDataType = list[dict[str, Any]]
MetricDataType = dict[str, dict[str, float]]
ValueListType = dict[str, list[float]]

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

# ▼△▼△▼△▼△▼△▼△▼△▼△▼△ Pseudocodigo △▼△▼△▼△▼△▼△▼△▼△▼△▼

public
static
Dict[String, Any]
auditarCalidadAvanzada(List[Dict[String, Any]]
datos,
Optional[String]
colFechaNacimiento = null,
Optional[List[String]]
columnasNumericas = null,
Optional[List[String]]
columnasTexto = null)
"""
Realiza un análisis completo de calidad de datos con opciones avanzadas

Args:
    datos: Lista de diccionarios representando filas de datos
    colFechaNacimiento: Columna específica para análisis de coherencia de fechas
    columnasNumericas: Lista de columnas a tratar como numéricas
    columnasTexto: Lista de columnas a tratar como de texto

Returns:
    Diccionario con todos los resultados de calidad ampliados
"""
var
resultados = QualityAuditor.auditarCalidad(datos)

# Análisis de fechas si se especifica una columna
if colFechaNacimiento != null & & !colFechaNacimiento.trim().isEmpty()
var
erroresFechas = DateAnalyzer.verificarCoherenciaFechas(datos, colFechaNacimiento)
resultados["analisis_fechas"] = dict()
resultados["analisis_fechas"]["columna_fecha"] = colFechaNacimiento
resultados["analisis_fechas"]["errores"] = erroresFechas
resultados["analisis_fechas"]["total_errores"] = erroresFechas.size()

# Análisis estadístico detallado si se especifican columnas numéricas
if columnasNumericas != null & & !columnasNumericas.isEmpty()
var
valoresNumericos = StatisticalAnalyzer.obtenerValoresNumericos(datos)
var
estadisticosDetallados = dict()

for String col in columnasNumericas
    if valoresNumericos.containsKey(col)
        var
        valores = valoresNumericos[col]
        var
        estadisticos = dict()

        # Calcular percentiles
        if !valores.isEmpty()
        var
        valoresOrdenados = sorted(valores)
        var
        size = valoresOrdenados.size()

        estadisticos["min"] = valoresOrdenados[0]
        estadisticos["max"] = valoresOrdenados[size - 1]
        estadisticos["media"] = sum(valoresOrdenados) / size

        # Mediana
        var
        medio = size / 2
        if size % 2 == 0
            estadisticos["mediana"] = (valoresOrdenados[medio - 1] + valoresOrdenados[medio]) / 2.0
        else
            estadisticos["mediana"] = valoresOrdenados[medio]

        # Percentiles
        estadisticos["q25"] = valoresOrdenados[Math.floor(size * 0.25)]
        estadisticos["q75"] = valoresOrdenados[Math.floor(size * 0.75)]

    estadisticosDetallados[col] = estadisticos

resultados["estadisticos_detalles"] = estadisticosDetallados

return resultados

public
static
Dict[String, int]
obtenerMetricasGenerales(List[Dict[String, Any]]
datos)
"""
Obtiene métricas generales de calidad de datos

Args:
    datos: Lista de diccionarios representando filas de datos

Returns:
    Diccionario con métricas generales de calidad
"""
var
metricas = dict()

if datos == null | | datos.isEmpty()
    metricas["total_filas"] = 0
    metricas["total_columnas"] = 0
    metricas["calidad_general"] = 0.0
    return metricas

# Obtener información básica
var
conteoNulos = NullAnalyzer.contarNulos(datos)
var
conteoTotalFilas = datos.size()

# Calcular métricas
metricas["total_filas"] = conteoTotalFilas
metricas["total_columnas"] = conteoNulos.keySet().size()

# Calcular calidad general basada en nulos
var
totalNulos = 0
for int conteo in conteoNulos.values()
    totalNulos += conteo

var
totalPosiblesNulos = conteoTotalFilas * conteoNulos.keySet().size()
var
porcentajeNulos = 0.0
if totalPosiblesNulos > 0
    porcentajeNulos = (totalNulos / totalPosiblesNulos) * 100.0

metricas["porcentaje_datos_nulos"] = round(porcentajeNulos, 2)
metricas["calidad_general"] = round(100.0 - porcentajeNulos, 2)

# Métricas de unicidad
var
unicidad = UniquenessAnalyzer.calcularUnicidad(datos)
var
promedioUnicidad = 0.0
if !unicidad.isEmpty()
var
sumaUnicidad = 0.0
for float valor in unicidad.values()
    sumaUnicidad += valor
promedioUnicidad = sumaUnicidad / unicidad.size()

metricas["promedio_unicidad"] = round(promedioUnicidad, 2)

return metricas

public
static
List[String]
generarAlertas(List[Dict[String, Any]]
datos,
Optional[float]
umbralNulos = 50.0,
Optional[float]
umbralUnicidadBaja = 10.0,
Optional[float]
umbralUnicidadAlta = 95.0)
"""
Genera alertas basadas en umbrales de calidad

Args:
    datos: Lista de diccionarios representando filas de datos
    umbralNulos: Porcentaje de nulos que dispara alerta
    umbralUnicidadBaja: Porcentaje de unicidad baja que dispara alerta
    umbralUnicidadAlta: Porcentaje de unicidad alta que dispara alerta

Returns:
    Lista de mensajes de alerta
"""
var
alertas = list()

if datos == null | | datos.isEmpty()
    alertas.append("ALERTA: No hay datos para analizar")
    return alertas

# Análisis de nulos
var
conteoNulos = NullAnalyzer.contarNulos(datos)
var
totalFilas = datos.size()

for String columna in conteoNulos.keySet()
    var
    nulos = conteoNulos[columna]
    var
    porcentajeNulos = (nulos / totalFilas) * 100.0

    if porcentajeNulos >= umbralNulos
        var
        mensaje = "ALERTA: Columna '" + columna + "' tiene " + \
                  round(porcentajeNulos, 2) + "% de valores nulos (umbral: " + \
                  umbralNulos + "%)"
        alertas.append(mensaje)

# Análisis de unicidad
var
unicidad = UniquenessAnalyzer.calcularUnicidad(datos)

for String columna in unicidad.keySet()
    var
    porcentajeUnicidad = unicidad[columna]

    if porcentajeUnicidad <= umbralUnicidadBaja
        var
        mensaje = "ALERTA: Columna '" + columna + "' tiene baja unicidad: " + \
                  round(porcentajeUnicidad, 2) + "% (umbral bajo: " + \
                  umbralUnicidadBaja + "%)"
        alertas.append(mensaje)
    else if porcentajeUnicidad >= umbralUnicidadAlta
    var
    mensaje = "ALERTA: Columna '" + columna + "' tiene alta unicidad: " + \
              round(porcentajeUnicidad, 2) + "% (umbral alto: " + \
              umbralUnicidadAlta + "%) - posible clave primaria"
    alertas.append(mensaje)

return alertas