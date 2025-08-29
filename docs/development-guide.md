# Development Guide

This document explains how to work with the development environment, linting, and CI/CD pipeline.

## Setup Development Environment

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

2. **Run tests:**
   ```bash
   python -m unittest discover tests -v
   ```

## Code Quality Tools

### Linting with flake8
```bash
# Check for syntax errors (strict)
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# General linting (warnings only)
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
```

### Code formatting with black
```bash
# Check formatting
black --check --diff --line-length=127 .

# Auto-format code
black --line-length=127 .
```

### Import sorting with isort
```bash
# Check import sorting
isort --check-only --diff .

# Auto-sort imports
isort .
```

### Run all quality checks
```bash
# Run the same checks as CI
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
black --check --diff --line-length=127 . || echo "Formatting suggestions available"
isort --check-only --diff . || echo "Import sorting suggestions available"
python -m unittest discover tests -v
```

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs automatically on:
- Push to `main` or `dev` branches
- Pull requests to `main` or `dev` branches

### What the CI checks:
1. **Python syntax errors** (fails build)
2. **Undefined names and imports** (fails build)
3. **Unit tests** (fails build)
4. **Application startup** (fails build)
5. **Code formatting** (informational warnings)
6. **Import sorting** (informational warnings)

### CI Pipeline Features:
- Python 3.12 support
- Dependency caching for faster builds
- Parallel linting and testing
- Comprehensive error reporting

## Configuration Files

- **`.flake8`**: Flake8 linting configuration
- **`pyproject.toml`**: Black, isort, and pytest configuration
- **`requirements-dev.txt`**: Development dependencies
- **`.github/workflows/ci.yml`**: CI/CD pipeline configuration

## Best Practices

1. **Before committing:**
   - Run tests: `python -m unittest discover tests -v`
   - Check for syntax errors: `flake8 . --select=E9,F63,F7,F82`

2. **Code formatting (recommended):**
   - Format code: `black --line-length=127 .`
   - Sort imports: `isort .`

3. **Writing tests:**
   - Place test files in the `tests/` directory
   - Name test files with `test_` prefix
   - Use `unittest.TestCase` or `unittest.IsolatedAsyncioTestCase` for async tests

## Troubleshooting

### Common CI failures:
- **Import errors**: Check that all imports are available and properly installed
- **Test failures**: Run tests locally first: `python -m unittest discover tests -v`
- **Syntax errors**: Use flake8 to identify: `flake8 . --select=E9,F63,F7,F82`

### Local development issues:
- **Missing dependencies**: Install dev requirements: `pip install -r requirements-dev.txt`
- **Database connection errors**: Tests use mocked dependencies, should not require real database