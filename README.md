# Auditor de Calidad de Datos Integrado

Sistema integral de auditoría de calidad de datos con soporte para validación de esquema, análisis de calidad avanzado y configuración flexible mediante YAML. Ideal para pipelines de datos automatizados que requieren validación robusta y monitoreo de calidad.

## Descripción

Sistema completo que combina validación de esquema CSV y auditoría avanzada de calidad de datos:

### Validación de Esquema
- Presencia de encabezados esperados
- Tipos de datos correctos por columna
- Valores nulos en campos requeridos
- Restricciones y patrones personalizados

### Auditoría de Calidad
- **Análisis de Nulos**: Detección y cuantificación de valores faltantes
- **Análisis de Unicidad**: Identificación de duplicados y valores únicos
- **Análisis Estadístico**: Métricas descriptivas y detección de outliers
- **Análisis de Fechas**: Validación de coherencia temporal
- **Análisis de Texto**: Métricas de longitud y calidad de cadenas
- **Generación de Alertas**: Umbrales configurables para notificaciones

## Características Principales

* ✅ **Validación de Esquema**: Verificación estructural contra esquemas YAML
* ✅ **Análisis de Calidad**: 5 tipos de análisis especializados
* ✅ **Configuración Flexible**: Reglas definidas en YAML con umbrales personalizables
* ✅ **Generación de Informes**: Múltiples formatos (JSON, TXT, HTML)
* ✅ **Pipeline Integrado**: Flujo completo de procesamiento con `pipeline.yaml`
* ✅ **Transformación de Datos**: Conversión automática de tipos
* ✅ **Manejo de Exclusiones**: Filtrado de columnas y valores específicos
* ✅ **Alertas Configurables**: Niveles de advertencia y críticos
* ✅ **Clean Architecture**: Diseño modular y extensible
* ✅ **Bibliotecas Estándar**: Sin dependencias externas

## Requisitos

- Python 3.6+
- Solo librerías estándar de Python (sin dependencias externas)

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/Fisherk2/auditor-de-calidad-de-datos
cd auditor-de-calidad-de-datos

# El sistema está listo para usar (no requiere instalación adicional)
```

## Uso

### Auditoría de Calidad con Configuración Predeterminada

```python
from src import QualityAuditor, CSVReader

# Leer datos desde CSV
reader = CSVReader()
data = list(reader.read_rows("data/input/sample_data.csv"))

# Ejecutar auditoría con configuración por defecto
results = QualityAuditor.quality_audit(data)

print(f"Total de filas: {results['total_rows']}")
print(f"Análisis de nulos: {results['null_analysis']}")
print(f"Análisis de unicidad: {results['uniqueness_analysis']}")
```

### Auditoría con Configuración Personalizada

```python
from src import QualityAuditor, CSVReader, QualityReport

# Leer datos
reader = CSVReader()
data = list(reader.read_rows("data/input/sample_data.csv"))

# Ejecutar auditoría con reglas personalizadas
results = QualityAuditor.quality_audit(data, "schemas/quality_rules.yaml")

# Generar informe completo
report = QualityReport.generate_report(results, "data/output/quality_report.json")
print("Informe generado en:", report)
```

### Transformación de Datos

```python
from src import DataParser, QualityRulesReader, CSVReader, QualityAuditor

# Cargar datos y reglas
reader = CSVReader()
data = list(reader.read_rows("data/input/sample_data.csv"))

config = QualityRulesReader.load_configs("schemas/quality_rules.yaml")
data_type_rules = config.get('quality_rules', {}).get('data_types', {})

# Transformar tipos de datos automáticamente
transformed_data = DataParser.transform_data(data, data_type_rules)

# Ejecutar auditoría sobre datos transformados
results = QualityAuditor.quality_audit(transformed_data, "schemas/quality_rules.yaml")
```

### Generación de Informes

```python
from src import QualityReport, QualityAuditor, CSVReader

# Primero obtener los resultados de la auditoría
reader = CSVReader()
data = list(reader.read_rows("data/input/sample_data.csv"))
results = QualityAuditor.quality_audit(data, "schemas/quality_rules.yaml")

# Generar diferentes tipos de informes
# Informe JSON completo (retorna string)
json_report = QualityReport.generate_json_report(results)
print("JSON Report:", json_report)

# Informe resumido (retorna string)
summary_report = QualityReport.generate_summary_report(results)
print("Summary Report:", summary_report)

# Informe detallado (retorna string)
detailed_report = QualityReport.generate_detail_report(results)
print("Detailed Report:", detailed_report)

# Guardar informes en archivos
# Guardar informe JSON
QualityReport.save_report(results, "data/output/quality_report.json", "json")

# Guardar informe resumido
QualityReport.save_report(results, "data/output/quality_summary.txt", "summary")

# Guardar informe detallado
QualityReport.save_report(results, "data/output/quality_detailed.txt", "detailed")

# Guardar informe con timestamp automático
timestamped_file = QualityReport.save_report_with_timestamp(
    results, 
    "data/output/quality_report", 
    "json"
)
print("Informe guardado en:", timestamped_file)

# Generar informe de alertas específico
alerts_report = QualityReport.generate_alerts_report(data, "schemas/quality_rules.yaml")
print("Alerts:", alerts_report)
```

### Pipeline Completo

```python
# Usar el archivo pipeline.yaml.example como plantilla
from src import PipelineExecutor  # (clase a implementar)

# Ejecutar pipeline completo
executor = PipelineExecutor("pipeline.yaml.example")
results = executor.run()
```

### Validación de Esquema CSV

```python
from src import CSVValidator, SchemaValidator

# Validación básica de esquema
validator = CSVValidator()
schema_validator = SchemaValidator()

# Cargar esquema desde archivo YAML
schema = schema_validator.load_schema_from_yaml("schemas/default_schema.yaml")

# Validar archivo CSV contra esquema
errores = validator.validate_file("data/input/sample_data.csv", schema)

# Mostrar errores encontrados
for error in errores:
    print(error)
```

### Validación con Esquema Personalizado

```python
from src import CSVValidator

# Definir esquema directamente en código
esquema_personalizado = {
    "id": {"tipo": "entero", "requerido": True},
    "nombre": {"tipo": "cadena", "requerido": True},
    "email": {"tipo": "cadena", "requerido": False},
    "edad": {"tipo": "entero", "requerido": False},
    "salario": {"tipo": "flotante", "requerido": False},
    "activo": {"tipo": "booleano", "requerido": True}
}

validator = CSVValidator()
errores = validator.validate_file("data/input/sample_data.csv", esquema_personalizado)

if not errores:
    print("✅ Archivo CSV válido")
else:
    print(f"❌ Se encontraron {len(errores)} errores:")
    for error in errores:
        print(f"  - {error}")
```

### Tipos de Datos Soportados

El validador de esquema soporta los siguientes tipos de datos:

- **"entero"**: Valores numéricos enteros (ej: 1, 42, -10)
- **"flotante"**: Valores numéricos decimales (ej: 3.14, -0.5, 100.0)
- **"cadena"**: Cadenas de texto (ej: "Juan", "Hola Mundo")
- **"booleano"**: Valores verdadero/falso (ej: true, false, 1, 0)

### Errores de Validación Comunes

El sistema detecta y reporta los siguientes tipos de errores:

```python
# Ejemplos de mensajes de error generados:
errores_típicos = [
    "fila 5: campo requerido 'nombre' está vacío",
    "fila 12: valor entero no válido en columna 'edad': 'abc'",
    "fila 8: valor flotante no válido en columna 'salario': 'mil'",
    "fila 3: valor booleano no válido en columna 'activo': 'quizás'",
    "archivo: campo 'telefono' no encontrado en esquema",
    "archivo: campo requerido 'id' no encontrado en CSV"
]
```

## Estructura del Proyecto

```
auditor-de-calidad-de-datos/
├── src/                          # Código fuente principal
│   ├── quality_auditor/          # Módulos de análisis de calidad
│   │   ├── main_auditor.py       # Orquestador principal
│   │   ├── null_analyzer.py      # Análisis de valores nulos
│   │   ├── uniqueness_analyzer.py # Análisis de unicidad
│   │   ├── statistical_analyzer.py # Análisis estadístico
│   │   └── date_analyzer.py      # Análisis de fechas
│   ├── readers/                  # Lectores de datos y configuración
│   │   ├── csv_reader.py         # Lector de archivos CSV
│   │   └── quality_rules_reader.py # Lector de reglas YAML
│   ├── utils/                    # Utilidades y generadores
│   │   ├── data_parser.py        # Transformación de datos
│   │   ├── quality_report.py     # Generador de informes
│   │   ├── date_helper.py        # Utilidades de fechas
│   │   └── csv_error_reporter.py # Reporte de errores CSV
│   ├── validators/               # Validadores (sistema original)
│   │   ├── csv_validator.py      # Validador principal de CSV
│   │   ├── type_validator.py     # Validador de tipos de datos
│   │   └── schema_validator.py   # Validador de esquemas YAML
│   └── __init__.py               # Exportaciones del paquete
├── schemas/                      # Archivos de configuración
│   ├── quality_rules.yaml        # Reglas de calidad de datos
│   └── default_schema.yaml       # Esquema de validación CSV
├── data/                         # Datos de ejemplo y salida
│   ├── input/                    # Datos de entrada
│   │   └── sample_data.csv       # Ejemplo de datos
│   └── output/                   # Resultados generados
├── test/                         # Suite de pruebas
│   ├── test_quality_auditor.py   # Pruebas del sistema de calidad
│   └── test_csv_validator.py     # Pruebas del validador CSV
├── samples/                      # Archivos de ejemplo para pruebas
│   ├── valid_sample.csv          # CSV válido para pruebas
│   └── invalid_sample.csv        # CSV inválido para pruebas
├── pipeline.yaml.example         # Plantilla de pipeline integrado
├── README.md                     # Documentación
└── CONTRIBUTING.md               # Guía de contribución
```

## Configuración

### Archivo de Esquema CSV (`schemas/default_schema.yaml`)

Define la estructura esperada del archivo CSV y tipos de datos:

```yaml
# Esquema de validación para archivos CSV
id:
  tipo: "entero"
  requerido: true

nombre:
  tipo: "cadena"
  requerido: true

apellido:
  tipo: "cadena"
  requerido: false

edad:
  tipo: "entero"
  requerido: false

salario:
  tipo: "flotante"
  requerido: false

activo:
  tipo: "booleano"
  requerido: true

fecha_registro:
  tipo: "cadena"
  requerido: false

email:
  tipo: "cadena"
  requerido: false
```

**Propiedades del Esquema:**
- **tipo**: Tipo de dato esperado ("entero", "flotante", "cadena", "booleano")
- **requerido**: Si el campo es obligatorio (true/false)

### Archivo de Reglas de Calidad (`schemas/quality_rules.yaml`)

Define las reglas para análisis de calidad:

```yaml
quality_rules:
  data_types:
    numeric:
      type: "number"
      allow_decimals: true
    text:
      type: "string"
      max_length: 255
    date:
      type: "date"
      format: "%Y-%m-%d"
  
  null_rules:
    null_values: ["", "NULL", "N/A", "null", "None"]
  
  general_rules:
    min_uniqueness_percentage: 5.0
    max_uniqueness_percentage: 95.0
  
  exclusion_rules:
    exclude_columns: ["temp_field"]
    exclude_values:
      status: ["DELETED"]
```

### Generación de Informes (`src/utils/quality_report.py`)

El sistema genera múltiples tipos de informes:

- **JSON**: Estructurado para consumo programático
- **TXT**: Legible para revisión humana
- **HTML**: Interactivo con visualizaciones
- **CSV**: Para análisis en hojas de cálculo

Los informes incluyen:
- Métricas de calidad por columna
- Alertas basadas en umbrales
- Estadísticas descriptivas
- Recomendaciones de mejora

## Pipeline de Datos

### Archivo de Configuración (`pipeline.yaml.example`)

El sistema incluye una plantilla para pipelines completos que integra validación y auditoría:

```yaml
# Flujo completo: preprocessing → validation → quality_audit → postprocessing → output
execution:
  pipeline_order:
    - "preprocessing"
    - "validation" 
    - "quality_audit"
    - "postprocessing"
    - "output"

variables:
  base_input_dir: "data/input"
  base_output_dir: "data/output"
  base_schemas_dir: "schemas"

input:
  primary_source:
    type: "csv"
    path: "${base_input_dir}/sample_data.csv"

validation:
  enabled: true
  schema_path: "${base_schemas_dir}/default_schema.yaml"

quality_audit:
  enabled: true
  rules_path: "${base_schemas_dir}/quality_rules.yaml"

output:
  validation_results:
    formats: ["json", "txt"]
  quality_results:
    formats: ["json", "txt", "html"]
```

### Ejecución del Pipeline

```python
# Ejecutar pipeline completo (requiere implementación de PipelineExecutor)
from src import PipelineExecutor

executor = PipelineExecutor("pipeline.yaml.example")
results = executor.run()

# Acceder a resultados
validation_results = results['validation']
quality_results = results['quality_audit']
output_files = results['output']
```

## Pruebas

El sistema incluye suites completas de pruebas para ambos componentes:

### Pruebas del Sistema de Calidad

```bash
# Ejecutar todas las pruebas de calidad
python test/test_quality_auditor.py

# Resultado esperado: 12/12 tests passed
```

Las pruebas cubren:
- Análisis individual de cada componente (NullAnalyzer, UniquenessAnalyzer, etc.)
- Integración completa del sistema
- Casos límite y manejo de errores
- Transformación de datos
- Generación de informes

### Pruebas del Validador CSV

```bash
# Ejecutar todas las pruebas del validador
python test/test_csv_validator.py

# Resultado esperado: 6/6 tests passed
```

Las pruebas cubren:
- ✅ Validación de CSV correcto contra esquema
- ✅ Detección de campos requeridos faltantes
- ✅ Validación de tipos de datos incorrectos
- ✅ Detección de valores nulos en campos requeridos
- ✅ Manejo de archivos no existentes
- ✅ Detección de campos no permitidos en el esquema

### Ejecución Completa de Pruebas

```bash
# Ejecutar ambas suites de pruebas
python test/test_quality_auditor.py && echo "---" && python test/test_csv_validator.py

# Salida esperada:
# 🚀 Starting Quality Auditor Test Suite
# ✅ 12/12 tests passed
# ---
# 🮙🮘🮙🮘🮙🮙🮘🮙🮙🮙🮙🮙🮙 Ejecutando pruebas del validador de CSV 🮙🮘🮙🮙🮙🮙🮘🮙🮙🮙🮙🮙🮙🮙🮙🮙🮙🮙🮙
# ✅ 6/6 tests passed
```

## Formato del Esquema

El esquema define las expectativas para cada columna:

```yaml
tipo: "entero", "flotante", "cadena", "booleano"
requerido: True o False
```

## Salida de Errores

La validación de esquema retorna mensajes en formato:

```
"fila X: campo 'nombre_campo' - mensaje_de_error"
```

Ejemplos:
```
"fila 12: valor no numérico en columna 'ingresos'"
"fila 5: campo requerido 'nombre' está vacío"
"archivo: campo 'apellido' no encontrado en esquema"
```

## Características Técnicas

* ✅ **Clean Architecture**: Diseño modular y desacoplado
* ✅ **Clean Code**: Código legible y mantenible
* ✅ **Testing FIRST**: Pruebas automáticas completas
* ✅ **Configuración Externa**: Reglas en YAML, no hardcodeadas
* ✅ **Extensibilidad**: Fácil agregar nuevos analizadores
* ✅ **Rendimiento**: Optimizado para datasets grandes

## Contribución

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

Asegúrate de seguir los principios de Clean Architecture y Clean Code, y de ejecutar las pruebas antes de enviar.

## Autores

- **Fisherk2** - *Desarrollo inicial y arquitectura*

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

**¿Necesitas ayuda?** 

- Revisa la [guía de contribución](CONTRIBUTING.md)
- Ejecuta las pruebas para entender el sistema: `python test/test_quality_auditor.py`
- Explora los ejemplos en `data/input/sample_data.csv` y `schemas/quality_rules.yaml`