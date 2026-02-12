# CSV Validator for Data Pipelines

## Overview
A lightweight Python component that validates CSV files against a predefined schema, ensuring data integrity before processing in data pipelines. The validator detects and reports common issues in structure, data types, and missing values.

## Features
- Schema-based CSV validation
- Data type verification (int, float, string, boolean)
- Required field validation
- Detailed error reporting with specific row and column locations
- Support for flexible schema definitions using dictionaries

## Requirements
- Python 3.6+
- Standard libraries only (no external dependencies)

## Installation
```bash
# Clone the repository
git clone https://github.com/Fisherk2/auditor-de-calidad-de-datos
cd csv-validator
```

## Usage Example
```python
from src.validators.csv_validator import CSVValidator

# Define expected schema
schema = {
    "id": {"type": "integer", "required": True},
    "name": {"type": "string", "required": True},
    "income": {"type": "float", "required": False}
}

# Validate CSV file
validator = CSVValidator()
errors = validator.validate_file("path/to/file.csv", schema)

if errors:
    for error in errors:
        print(f"Error: {error}")
else:
    print("CSV validation passed!")
```

## Project Structure
```bash
.
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── requirements.txt
├── samples/
│   ├── valid_sample.csv
│   └── invalid_sample.csv
├── schemas/
│   └── default_schema.yaml
├── src/
│   ├── __init__.py
│   ├── validators/
│   │   ├── __init__.py
│   │   ├── csv_validator.py
│   │   ├── type_validator.py
│   │   └── schema_validator.py
│   ├── readers/
│   │   ├── __init__.py
│   │   └── csv_reader.py
│   └── utils/
│       ├── __init__.py
│       └── error_reporter.py
└── tests/
    ├── __init__.py
    └── test_csv_validator.py
```

## Schema Definition
The schema defines expected columns with their types and required status:

- `type`: Expected data type ("integer", "float", "string", "boolean")
- `required`: Boolean indicating if the field is mandatory

## License
MIT License - See LICENSE file for details