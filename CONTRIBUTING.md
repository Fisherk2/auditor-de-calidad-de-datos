# Contributing to CSV Validator for Data Pipelines

Thank you for your interest in contributing to this project! This document outlines the process for contributing code, bug reports, and feature requests.

## How to Contribute

### Reporting Bugs
1. Search the issue tracker to see if the bug has already been reported
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce the issue
   - Expected vs actual behavior
   - Environment information (Python version, OS, etc.)

### Suggesting Features
1. Open an issue describing the feature request
2. Explain the problem the feature would solve
3. Provide examples of how the feature would be used

### Submitting Code Changes
1. Fork the repository
2. Create a new branch for your feature/bug fix
3. Write tests for your changes
4. Follow the existing code style and architecture patterns
5. Submit a pull request with clear description of changes

## Development Setup

1. Clone your forked repository
2. Navigate to the project directory
3. Install dependencies: `pip install -r requirements.txt` (though this project uses only standard libraries)
4. Run tests: `python -m pytest tests/`

## Code Style Guidelines

- Follow PEP 8 style guide
- Write docstrings for all public methods and classes
- Keep functions focused and single-purpose
- Use descriptive variable and function names
- Maintain separation of concerns between components

## Architecture Guidelines

This project follows these architectural principles:
- Single Responsibility: Each class has one reason to change
- Dependency Injection: Components are loosely coupled
- Testability: Code should be easily testable
- Maintainability: Code should be readable and well-documented

## Testing Requirements

- All new features must include unit tests
- Bug fixes should include regression tests
- Test coverage should remain high
- Tests should verify both positive and negative scenarios

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Add appropriate tests for new functionality
3. Ensure all tests pass
4. Verify that your code follows the style guidelines
5. Submit the pull request with a clear description