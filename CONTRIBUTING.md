# Guía de Contribución - Auditor de Calidad de Datos

¡Gracias por tu interés en contribuir al sistema de auditoría de calidad de datos y validador de esquemas CSV! Este proyecto combina validación estructural de archivos CSV con análisis avanzado de calidad de datos, siguiendo principios de Clean Architecture y Clean Code.

## 🎯 Visión del Proyecto

Este sistema proporciona:
- **Validación de Esquemas CSV**: Verificación estructural contra esquemas YAML
- **Auditoría de Calidad**: Análisis de nulos, unicidad, estadísticas, fechas y texto
- **Configuración Flexible**: Reglas definidas externamente en YAML
- **Informes Detallados**: Múltiples formatos de salida (JSON, TXT, HTML)
- **Arquitectura Modular**: Diseño extensible y mantenible

## 📋 Antes de Contribuir

### Conocimientos Requeridos

Antes de contribuir, familiarízate con:

#### **Principios de Diseño**
- **Clean Architecture**: Separación de capas y dependencias
- **SOLID Principles**: SRP, OCP, LSP, ISP, DIP
- **Design Patterns**: Strategy, Factory, Observer
- **Clean Code**: Código legible y mantenible

#### **Estructura del Proyecto**
- **Paquetes Modulares**: Cada componente tiene una responsabilidad clara
- **Inyección de Dependencias**: Sin hardcode de dependencias
- **Configuración Externa**: Reglas en YAML, no en código
- **Testing FIRST**: Pruebas que guían el desarrollo

#### **Tecnologías**
- **Python 3.6+**: Solo bibliotecas estándar
- **YAML**: Para archivos de configuración
- **Markdown**: Para documentación
- **Type Hints**: Para tipado explícito

## 🚀 Cómo Contribuir

### Reporte de Bugs
- Usa el issue tracker para reportar bugs
- Incluye un título claro y descripción detallada
- Proporciona pasos paso a paso para reproducir el bug
- Incluye información del entorno (OS, versión Python, etc.)
- Adjunta archivos de configuración y datos de ejemplo si aplica

### Sugerencias de Features
- Abre un issue con explicación detallada del feature
- Describe el caso de uso y beneficios
- Considera el impacto en la funcionalidad existente
- Propón cómo se integraría con la arquitectura actual

### Contribuciones de Código

#### **Flujo de Trabajo**
1. Fork del repositorio
2. Crear rama de feature (`git checkout -b feature/amazing-feature`)
3. Hacer cambios siguiendo los estándares de código
4. Agregar pruebas para nueva funcionalidad
5. Ejecutar suite de pruebas para asegurar que todo pasa
6. Commit de cambios (`git commit -m 'Add amazing feature'`)
7. Push a la rama (`git push origin feature/amazing-feature`)
8. Abrir Pull Request

#### **Tipos de Contribuciones**

##### 🔍 **Añadir Nuevos Analizadores**
Para añadir un nuevo analizador de calidad:

```python
# 1. Crear nuevo analizador en src/quality_auditor/
# src/quality_auditor/new_analyzer.py
class NewAnalyzer:
    @staticmethod
    def analyze(data: RowDataType, config: dict[str, Any]) -> dict[str, Any]:
        # Implementar lógica de análisis
        return results

# 2. Integrar en main_auditor.py
# Agregar en QualityAuditor.quality_audit():
results["new_analysis"] = NewAnalyzer.analyze(filtered_data, config)

# 3. Actualizar quality_report.py
# Agregar sección en generate_summary_report() y generate_detail_report()
```

##### 📋 **Extender Lectores de Configuración**
Para añadir nuevos tipos de configuración:

```python
# 1. Extender src/readers/quality_rules_reader.py
class QualityRulesReader:
    @staticmethod
    def load_new_config_type(path: str) -> dict[str, Any]:
        # Implementar carga de nueva configuración
        return config

# 2. Actualizar esquema YAML con nuevas secciones
# schemas/quality_rules.yaml
new_config_type:
  rules:
    # Nuevas reglas
```

##### 🔧 **Integrar con Validadores CSV**
Para añadir validaciones al sistema CSV:

```python
# 1. Extender src/validators/csv_validator.py
class CSVValidator:
    def validate_new_feature(self, filepath: str, schema: SchemaDefinition) -> list[str]:
        # Implementar nueva validación
        return errors

# 2. Actualizar src/validators/type_validator.py si es necesario
# 3. Actualizar src/utils/csv_error_reporter.py para nuevos tipos de errores
```

##### 📊 **Actualizar Generadores de Informes**
Para añadir nuevos tipos de informes:

```python
# 1. Extender src/utils/quality_report.py
class QualityReport:
    @staticmethod
    def generate_new_report_type(results: dict[str, Any]) -> str:
        # Implementar nuevo formato de informe
        return report_content

# 2. Actualizar save_report() para soportar nuevo formato
# 3. Agregar ejemplos en README.md
```

##### 🏗️ **Mantener Coherencia con Clean Architecture**
- **Regla de Dependencia**: Las dependencias apuntan hacia adentro
- **Aislamiento**: La lógica de negocio no depende de frameworks
- **Configuración Externa**: Sin hardcode de reglas de negocio
- **Pruebas Independientes**: Cada componente se puede probar en aislamiento

## 🎨 Guía de Estilo

### **Principios Generales**
- **Single Responsibility Principle (SRP)**: Cada clase tiene una razón para cambiar
- **Keep it Simple**: Funciones pequeñas y enfocadas
- **Clean Code**: El código se explica por sí mismo
- **Consistency**: Mantener coherencia con el código existente

### **Nomenclatura**
```python
# ✅ BUENO - Nombres descriptivos
class QualityAuditor:
    def analyze_null_values(self, data: RowDataType) -> dict[str, Any]:
        null_counts = {}
        return null_counts

# ❌ EVITAR - Nombres ambiguos
class QA:
    def proc(self, d) -> dict:
        nc = {}
        return nc
```

### **Tipado Explícito**
```python
# ✅ BUENO - Type hints completos
from typing import Dict, Any, Optional, List

def process_data(
    data: List[Dict[str, Any]], 
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    return results

# ❌ EVITAR - Sin tipado
def process_data(data, config=None):
    return results
```

### **Estructura de Clases**
```python
# ✅ BUENO - Estructura clara
class DataAnalyzer:
    """Clase para análisis de datos con configuración flexible."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
    
    def analyze(self, data: RowDataType) -> Dict[str, Any]:
        """Analiza los datos según configuración."""
        return self._perform_analysis(data)
    
    def _load_config(self, path: Optional[str]) -> Dict[str, Any]:
        """Carga configuración desde archivo YAML."""
        # Implementación privada
        pass
    
    def _perform_analysis(self, data: RowDataType) -> Dict[str, Any]:
        """Realiza el análisis principal."""
        # Implementación privada
        pass
```

### **Manejo de Errores**
```python
# ✅ BUENO - Manejo específico de errores
try:
    config = QualityRulesReader.load_configs(config_path)
except FileNotFoundError:
    raise ConfigError(f"Archivo de configuración no encontrado: {config_path}")
except yaml.YAMLError as e:
    raise ConfigError(f"Error al parsear YAML: {e}")

# ❌ EVITAR - Manejo genérico
try:
    config = QualityRulesReader.load_configs(config_path)
except:
    return None
```

### **Comentarios y Docstrings**
```python
# ✅ BUENO - Docstrings informativos
def calculate_uniqueness(data: RowDataType, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcula el porcentaje de valores únicos por columna.
    
    Args:
        data: Lista de diccionarios representando filas de datos
        config: Configuración con umbrales y reglas de análisis
        
    Returns:
        Diccionario con porcentajes de unicidad por columna
        
    Raises:
        ValueError: Si los datos están vacíos o son inválidos
    """
    pass

# ✅ BUENO - Comentarios solo cuando es necesario
class DataProcessor:
    def __init__(self):
        self._cache = {}  # Cache para resultados intermedios
        self._config = {}  # Configuración cargada externamente
```

### **Formato de Código**
- **Indentación**: 4 espacios (sin tabs)
- **Longitud de línea**: Máximo 100 caracteres
- **Imports**: Agrupados por tipo (standard library, third party, local)
- **Constantes**: En UPPER_CASE
- **Variables y funciones**: En snake_case
- **Clases**: En PascalCase

## 🧪 Pruebas

### **Principios de Testing**
- **Solo Bibliotecas Estándar**: No usar dependencias externas para pruebas
- **Testing FIRST**: Las pruebas guían el diseño del código
- **Aislamiento**: Cada prueba debe ser independiente
- **Cobertura Completa**: Probar casos normales, límite y error

### **Estructura de Pruebas**
```python
# ✅ BUENO - Estructura completa de prueba
class TestNewAnalyzer:
    """Suite de pruebas para el nuevo analizador."""
    
    def __init__(self):
        self.analyzer = NewAnalyzer()
        self.test_data = self._create_test_data()
        self.config = self._load_test_config()
    
    def test_normal_case(self) -> bool:
        """Prueba caso normal de funcionamiento."""
        try:
            results = self.analyzer.analyze(self.test_data, self.config)
            assert isinstance(results, dict), "Resultados deben ser diccionario"
            assert "new_analysis" in results, "Debe contener clave de análisis"
            print("✅ test_normal_case PASSED")
            return True
        except Exception as e:
            print(f"❌ test_normal_case FAILED: {e}")
            return False
    
    def test_edge_cases(self) -> bool:
        """Prueba casos límite."""
        # Datos vacíos
        empty_results = self.analyzer.analyze([], self.config)
        assert empty_results == {}, "Datos vacíos deben retornar diccionario vacío"
        
        # Configuración nula
        null_config_results = self.analyzer.analyze(self.test_data, None)
        assert isinstance(null_config_results, dict), "Config nula debe manejar gracefully"
        
        print("✅ test_edge_cases PASSED")
        return True
    
    def test_error_cases(self) -> bool:
        """Prueba manejo de errores."""
        try:
            # Datos inválidos
            invalid_data = [{"invalid": "structure"}]
            results = self.analyzer.analyze(invalid_data, self.config)
            # Debe manejar error sin lanzar excepción
            assert isinstance(results, dict), "Debe retornar diccionario incluso con error"
            print("✅ test_error_cases PASSED")
            return True
        except Exception as e:
            print(f"❌ test_error_cases FAILED: {e}")
            return False
    
    def _create_test_data(self) -> RowDataType:
        """Crea datos de prueba consistentes."""
        return [
            {"id": 1, "name": "test1", "value": 100},
            {"id": 2, "name": "test2", "value": 200}
        ]
    
    def _load_test_config(self) -> Dict[str, Any]:
        """Carga configuración de prueba."""
        return {"threshold": 0.5, "enabled": True}
```

### **Ejecución de Pruebas**
```bash
# Pruebas del sistema de calidad
python test/test_quality_auditor.py

# Pruebas del validador CSV
python test/test_csv_validator.py

# Ejecución completa
python test/test_quality_auditor.py && python test/test_csv_validator.py
```

### **Pruebas de Integración**
```python
# ✅ BUENO - Prueba de integración completa
def test_integration_quality_audit():
    """Prueba integración completa del sistema de calidad."""
    # 1. Cargar datos de prueba
    reader = CSVReader()
    data = list(reader.read_rows("samples/valid_sample.csv"))
    
    # 2. Ejecutar auditoría completa
    results = QualityAuditor.quality_audit(data, "schemas/quality_rules.yaml")
    
    # 3. Verificar estructura de resultados
    required_keys = ["total_rows", "null_analysis", "uniqueness_analysis", 
                     "statistical_analysis", "date_analysis"]
    for key in required_keys:
        assert key in results, f"Resultado debe contener {key}"
    
    # 4. Generar informe
    report = QualityReport.generate_summary_report(results)
    assert isinstance(report, str), "Informe debe ser string"
    assert len(report) > 0, "Informe no debe estar vacío"
    
    print("✅ test_integration_quality_audit PASSED")
```

### **Pruebas de Configuración**
```python
# ✅ BUENO - Prueba de carga de configuración
def test_config_loading():
    """Prueba carga y validación de configuración YAML."""
    try:
        # Configuración válida
        config = QualityRulesReader.load_configs("schemas/quality_rules.yaml")
        assert isinstance(config, dict), "Config debe ser diccionario"
        assert "quality_rules" in config, "Config debe contener quality_rules"
        
        # Configuración inválida
        with pytest.raises(FileNotFoundError):
            QualityRulesReader.load_configs("non_existent.yaml")
            
        print("✅ test_config_loading PASSED")
    except Exception as e:
        print(f"❌ test_config_loading FAILED: {e}")
```

## 📚 Documentación

### **Importancia de la Documentación**
La documentación es tan importante como el código. Ayuda a:
- Nuevos contribuidores a entender el sistema
- Usuarios a utilizar correctamente las funcionalidades
- Mantener la coherencia en el desarrollo
- Facilitar el mantenimiento a largo plazo

### **Tipos de Documentación**

#### **Docstrings de Código**
```python
# ✅ BUENO - Docstring completo
def analyze_data_quality(
    data: RowDataType, 
    config_path: Optional[str] = None,
    strict_mode: bool = False
) -> Dict[str, Any]:
    """
    Analiza la calidad de los datos según configuración YAML.
    
    Esta función coordina múltiples analizadores para evaluar diferentes
    aspectos de la calidad de datos: nulos, unicidad, estadísticas,
    coherencia de fechas y métricas de texto.
    
    Args:
        data: Lista de diccionarios representando filas de datos.
            Cada diccionario debe tener las mismas claves (columnas).
        config_path: Ruta opcional al archivo YAML con reglas de análisis.
            Si es None, usa configuración por defecto.
        strict_mode: Si es True, falla en errores críticos.
            Si es False, continúa procesamiento con advertencias.
    
    Returns:
        Diccionario con resultados completos del análisis:
        - 'total_rows': Número total de filas procesadas
        - 'null_analysis': Resultados del análisis de valores nulos
        - 'uniqueness_analysis': Resultados del análisis de unicidad
        - 'statistical_analysis': Resultados del análisis estadístico
        - 'date_analysis': Resultados del análisis de fechas
        - 'alerts': Lista de alertas generadas
    
    Raises:
        ConfigError: Si el archivo de configuración no es válido
        DataError: Si los datos de entrada son inválidos
        
    Example:
        >>> data = [{"id": 1, "name": "test"}, {"id": 2, "name": "demo"}]
        >>> results = analyze_data_quality(data, "schemas/quality_rules.yaml")
        >>> print(results['total_rows'])
        2
    """
    pass
```

#### **Actualización de README.md**
Cuando añades nuevas funcionalidades:
1. **Actualiza la sección "Características Principales"** con nuevos puntos
2. **Añade ejemplos de uso** en la sección "Uso"
3. **Actualiza la "Estructura del Proyecto"** si agregas nuevos archivos
4. **Documenta nuevas configuraciones** en la sección "Configuración"
5. **Añade información de pruebas** si es relevante

#### **Actualización de esta Guía**
Cuando modificas el sistema:
1. **Actualiza ejemplos de código** en las secciones correspondientes
2. **Añade nuevos patrones** si introduces nuevas formas de contribución
3. **Actualiza principios de arquitectura** si hay cambios estructurales
4. **Mantén coherencia** con el código actual

### **Formato de Documentación**
- **Markdown**: Para README.md y CONTRIBUTING.md
- **Docstrings**: Formato Google/NumPy recomendado
- **Comentarios**: Solo cuando el código no es autoexplicativo
- **Ejemplos**: Siempre incluir ejemplos funcionales

## 🏗️ Arquitectura

### **Principios Clave de Clean Architecture**

#### **Separación de Intereses (Separation of Concerns)**
```python
# ✅ BUENO - Cada capa tiene responsabilidad clara
# src/quality_auditor/main_auditor.py - Orquestación
class QualityAuditor:
    def quality_audit(self, data: RowDataType, config_path: Optional[str]) -> Dict[str, Any]:
        # Solo coordina, no implementa lógica específica
        
# src/quality_auditor/null_analyzer.py - Análisis específico
class NullAnalyzer:
    def count_nulls(self, data: RowDataType, config: Dict[str, Any]) -> Dict[str, Any]:
        # Solo implementa análisis de nulos
        
# src/utils/quality_report.py - Presentación
class QualityReport:
    def generate_summary_report(self, results: Dict[str, Any]) -> str:
        # Solo formatea y presenta resultados
```

#### **Inversión de Dependencias (Dependency Inversion)**
```python
# ✅ BUENO - Dependencias apuntan hacia adentro
# Las capas externas dependen de abstracciones, no de implementaciones

class DataProcessor:
    def __init__(self, analyzer_interface: AnalyzerInterface):
        # Depende de abstracción, no de implementación concreta
        self.analyzer = analyzer_interface

# ❌ EVITAR - Dependencia directa a implementación
class DataProcessor:
    def __init__(self):
        self.null_analyzer = NullAnalyzer()  # Dependencia directa
```

#### **Configuración Externa**
```python
# ✅ BUENO - Reglas en YAML, no hardcodeadas
# schemas/quality_rules.yaml
quality_rules:
  null_rules:
    null_values: ["", "NULL", "N/A"]
  thresholds:
    warning_percentage: 10.0

# ❌ EVITAR - Reglas hardcodeadas
class NullAnalyzer:
    def __init__(self):
        self.null_values = ["", "NULL", "N/A"]  # Hardcode
        self.warning_threshold = 10.0  # Hardcode
```

### **Estructura por Capas**

#### **Capa de Dominio (Domain Layer)**
```python
# src/quality_auditor/ - Lógica de negocio pura
# No depende de frameworks ni infraestructura
class NullAnalyzer:
    @staticmethod
    def count_nulls(data: RowDataType, config: Dict[str, Any]) -> Dict[str, Any]:
        # Lógica pura de análisis de nulos
        pass
```

#### **Capa de Aplicación (Application Layer)**
```python
# src/quality_auditor/main_auditor.py - Orquestación
# Coordina las capas de dominio
class QualityAuditor:
    @staticmethod
    def quality_audit(data: RowDataType, config_path: Optional[str]) -> Dict[str, Any]:
        # Orquesta múltiples analizadores
        pass
```

#### **Capa de Infraestructura (Infrastructure Layer)**
```python
# src/readers/ - Acceso a datos externos
# src/utils/ - Utilidades y presentación
class QualityRulesReader:
    @staticmethod
    def load_configs(path: str) -> Dict[str, Any]:
        # Acceso a archivos externos
        pass
```

### **Patrones Aplicados**

#### **Strategy Pattern**
```python
# Diferentes estrategias de análisis
class AnalyzerStrategy:
    def analyze(self, data: RowDataType, config: Dict[str, Any]) -> Dict[str, Any]:
        pass

class NullStrategy(AnalyzerStrategy):
    def analyze(self, data: RowDataType, config: Dict[str, Any]) -> Dict[str, Any]:
        return NullAnalyzer.count_nulls(data, config)

class UniquenessStrategy(AnalyzerStrategy):
    def analyze(self, data: RowDataType, config: Dict[str, Any]) -> Dict[str, Any]:
        return UniquenessAnalyzer.calculate_uniqueness(data, config)
```

#### **Single Responsibility Principle (SRP)**
```python
# ✅ BUENO - Cada clase tiene una responsabilidad
class NullAnalyzer:      # Solo analiza nulos
class UniquenessAnalyzer: # Solo analiza unicidad
class StatisticalAnalyzer: # Solo analiza estadísticas
class DateAnalyzer:       # Solo analiza fechas

# ❌ EVITAR - Clase con múltiples responsabilidades
class DataAnalyzer:
    def analyze_nulls(self): pass      # Responsabilidad 1
    def analyze_uniqueness(self): pass # Responsabilidad 2
    def generate_report(self): pass    # Responsabilidad 3
```

### **Beneficios de esta Arquitectura**
- **Testabilidad**: Cada componente se puede probar en aislamiento
- **Flexibilidad**: Fácil añadir nuevos analizadores sin modificar existentes
- **Mantenibilidad**: Cambios en una capa no afectan a otras
- **Extensibilidad**: Nuevas funcionalidades sin romprimir las existentes

## 🚀 Getting Started

### **Configuración del Entorno**
1. **Clone del repositorio**
   ```bash
   git clone https://github.com/Fisherk2/auditor-de-calidad-de-datos
   cd auditor-de-calidad-de-datos
   ```

2. **Verificar instalación**
   ```bash
   # El proyecto usa solo bibliotecas estándar de Python
   python --version  # Debe ser 3.6+
   ```

3. **Ejecutar pruebas para verificar setup**
   ```bash
   python test/test_quality_auditor.py
   python test/test_csv_validator.py
   ```

4. **Explorar el código**
   - Revisa `src/__init__.py` para ver las exportaciones disponibles
   - Examina `schemas/quality_rules.yaml` para entender la configuración
   - Mira `data/input/sample_data.csv` para datos de ejemplo

### **Primer Contribución**
1. **Elige un issue simple** o crea uno para mejora menor
2. **Fork y crea rama**: `git checkout -b feature/your-feature`
3. **Haz cambios** siguiendo esta guía
4. **Añade pruebas** para tu nueva funcionalidad
5. **Ejecuta todas las pruebas**: asegúrate que pasan
6. **Commit y push**: `git commit -m 'Add your feature'`
7. **Abre Pull Request** con descripción clara

## ❓ Preguntas Frecuentes

### **¿Cómo puedo empezar a contribuir?**
- Empieza con issues etiquetados como "good first issue"
- Lee el código existente para entender los patrones
- Ejecuta las pruebas para familiarizarte con el sistema

### **¿Qué tecnologías necesito conocer?**
- **Python 3.6+**: Lenguaje principal
- **YAML**: Para archivos de configuración
- **Markdown**: Para documentación
- **Clean Architecture**: Principios de diseño

### **¿Puedo añadir dependencias externas?**
- **No**: El proyecto usa solo bibliotecas estándar
- Si necesitas funcionalidad específica, impleméntala tú mismo
- Consulta antes si consideras que una dependencia es esencial

### **¿Cómo pruevo nuevos componentes?**
- Sigue el patrón de pruebas existentes en `test/`
- Usa solo bibliotecas estándar para testing
- Prueba casos normales, límite y error

### **¿Dónde debo documentar cambios?**
- **README.md**: Para funcionalidades visibles al usuario
- **Docstrings**: Para API interna y clases públicas
- **CONTRIBUTING.md**: Para cambios en el proceso de desarrollo
- **Comentarios**: Solo cuando el código no es autoexplicativo

## 💬 Contacto y Soporte

### **Obtener Ayuda**
- **Issues**: Para bugs y preguntas técnicas
- **Discussions**: Para ideas y debates de diseño
- **Pull Requests**: Para contribuciones de código

### **Reportar Problemas**
Al reportar un issue, incluye:
- **Descripción clara** del problema
- **Pasos para reproducir**
- **Entorno** (OS, Python version)
- **Archivos de ejemplo** si aplica
- **Logs o mensajes de error**

### **Sugerir Mejoras**
Al sugerir una feature:
- **Describe el caso de uso**
- **Explica los beneficios**
- **Considera el impacto** en el código existente
- **Propón una implementación** si es posible

## 🙏 Agradecimientos

¡Gracias por contribuir al proyecto! Tu ayuda hace que este sistema sea mejor para toda la comunidad.

### **Reconocimientos Especiales**
- A todos los contribuidores que han mejorado el código
- A quienes reportan bugs y sugieren mejoras
- A la comunidad que prueba y valida las funcionalidades

### **Principios de Comunidad**
- **Respeto**: Trata a todos con cortesía y profesionalismo
- **Colaboración**: Trabaja en equipo para lograr mejores resultados
- **Aprendizaje**: Comparte conocimiento y ayuda a otros crecer
- **Calidad**: Esfuérzate por mantener altos estándares de código

---

**¡Estamos emocionados de tener tu contribución! 🎉**

Si tienes alguna pregunta sobre cómo contribuir, no dudes en abrir un issue o contactar a los mantenedores del proyecto.

**Recuerda**: Cada contribución, por pequeña que sea, ayuda a hacer el proyecto mejor. ¡Gracias por tu tiempo y esfuerzo!