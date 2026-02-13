# Contributing to CSV Validator

Thank you for your interest in contributing to the CSV Validator project! All contributions are welcome and appreciated.

## How to Contribute

### Reporting Bugs
- Use the issue tracker to report bugs
- Include a clear title and description
- Provide step-by-step instructions to reproduce the bug
- Include your environment information (OS, Python version, etc.)

### Suggesting Features
- Open an issue with a detailed explanation of the feature
- Describe the use case and benefits
- Consider the impact on existing functionality

### Code Contributions
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following the coding standards below
4. Add tests for new functionality
5. Run the test suite to ensure everything passes
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Coding Standards

### General Principles
- Follow the Single Responsibility Principle (SRP)
- Keep functions small and focused
- Use descriptive names for variables, functions, and classes
- Write clean, readable code that serves as documentation

### Code Style
- Follow the existing code structure and patterns
- Use proper indentation (4 spaces)
- Maintain consistency with the existing codebase
- Write meaningful comments only when necessary

### Testing
- Write unit tests for all new functionality
- Ensure all tests pass before submitting a PR
- Aim for high test coverage, especially for critical paths

## Project Structure
```
src/
├── validators/          # Componentes de validación
│   ├── csv_validator.py
│   ├── type_validator.py
│   └── schema_validator.py
├── readers/             # Componentes de lectura
│   └── csv_reader.py
└── utils/               # Componentes utilitarios
    └── error_reporter.py
tests/                   # Suite de pruebas
└── test_csv_validator.py
```

## Getting Started

1. Clone the repository
2. Install dependencies (only standard library used)
3. Run the test suite to verify setup
4. Make your changes
5. Run tests again to ensure nothing broke

## Questions?

If you have any questions about contributing, feel free to open an issue or contact the maintainers.

Thank you for helping improve the CSV Validator!