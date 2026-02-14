# Changelog

Todos los cambios notables a este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto sigue [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-13

### Added
- Componente principal `CSVValidator` para validar archivos CSV contra esquemas
- Validación de encabezados, tipos de datos y campos requeridos
- Generación de reportes de errores detallados con ubicación específica
- Componentes modulares: `TypeValidator`, `SchemaValidator`, `CSVReader`, `ErrorReporter`
- Suite de pruebas unitarias completa
- Soporte para esquemas YAML y diccionarios Python
- Manejo seguro de excepciones y errores de lectura

### Changed
- Estructura modular para mejor mantenibilidad
- Validación estricta de tipos de datos
- Mensajes de error consistentes y descriptivos

### Fixed
- Validación segura de tipos y conversiones
- Manejo correcto de valores nulos y vacíos
- Prevención de ataques TOCTOU en pruebas