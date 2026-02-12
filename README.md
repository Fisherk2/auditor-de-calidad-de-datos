# Validador de CSV para Pipelines de Datos

Validador robusto que verifica la integridad de archivos CSV contra un esquema predefinido, ideal para pipelines de datos automatizados.

## Descripción

Esta herramienta permite validar archivos CSV verificando:
- Presencia de encabezados esperados
- Tipos de datos correctos por columna
- Valores nulos en campos requeridos
- Generación de reportes detallados de errores


## Requisitos
- Python 3.6+
- Solo librerías estándar de Python 

## Instalación
```bash
# Clone the repository
git clone https://github.com/Fisherk2/auditor-de-calidad-de-datos
cd csv-validator
```

## Uso
```python
from src.validators.csv_validator import CSVValidator

esquema = {
    "id": {"tipo": "entero", "requerido": True},
    "nombre": {"tipo": "cadena", "requerido": True},
    "ingresos": {"tipo": "flotante", "requerido": False}
}

validator = CSVValidator()
errores = validator.validate_file("ruta/al/archivo.csv", esquema)

for error in errores:
    print(error)
```

## Formato del Esquema
El esquema define las expectativas para cada columna:

    tipo: "entero", "flotante", "cadena", "booleano"
    requerido: True o False

## Salida de Errores
La función retorna una lista de strings con mensajes de error en formato:

    "fila X: campo 'nombre_campo' - mensaje_de_error"

Ejemplo de Error:

    "fila 12: valor no numérico en columna 'ingresos'"
    "fila 5: campo requerido 'nombre' está vacío"
    "archivo: campo 'apellido' no encontrado en esquema"

## Características

* ✅ Validación de tipos de datos 
* ✅ Manejo seguro de valores nulos 
* ✅ Reporte detallado con ubicación de errores 
* ✅ Compatible con pipelines automatizados 
* ✅ Uso de bibliotecas estándar de Python

## License
MIT License - Ver LICENSE para más detalles