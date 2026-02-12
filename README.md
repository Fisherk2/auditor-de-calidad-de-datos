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
- `src/validators/`: Core validation logic
- `src/readers/`: CSV reading utilities
- `src/utils/`: Error reporting and utility functions
- `samples/`: Sample CSV files for testing
- `schemas/`: Schema definition examples
- `tests/`: Unit tests

## License
MIT License - See LICENSE file for details