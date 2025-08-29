# Demarthology API

A FastAPI-based application for demarthology services with comprehensive CI/CD pipeline and code quality tools.

## Features

- **FastAPI** framework for high-performance API
- **MongoDB** with Beanie ODM for data persistence
- **Password security** with bcrypt hashing
- **Comprehensive testing** with unittest
- **Code quality** tools (flake8, black, isort)
- **CI/CD pipeline** with GitHub Actions

## Quick Start

### Prerequisites
- Python 3.12+
- pip

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd demarthology-api
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Run tests:**
   ```bash
   python -m unittest discover tests -v
   ```

4. **Start the application:**
   ```bash
   uvicorn main:app --reload
   ```

## Development

### Code Quality Checks

Run all quality checks (same as CI pipeline):
```bash
./scripts/check-quality.sh
```

Or run individual checks:

```bash
# Syntax errors (strict)
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# General linting
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Code formatting
black --check --diff --line-length=127 .

# Import sorting
isort --check-only --diff .

# Tests
python -m unittest discover tests -v
```

### Auto-format Code

```bash
# Format code
black --line-length=127 .

# Sort imports
isort .
```

## CI/CD Pipeline

The GitHub Actions workflow automatically runs on:
- Push to `main` or `dev` branches  
- Pull requests to `main` or `dev` branches

### Pipeline Stages:
1. **Setup** - Python 3.12, dependency caching
2. **Linting** - Syntax errors (strict), code style (warnings)
3. **Testing** - Unit tests, application startup verification
4. **Quality** - Code formatting and import sorting suggestions

### Build Status:
- ✅ **Passes**: No syntax errors, all tests pass
- ⚠️ **Warnings**: Code formatting suggestions (doesn't fail build)
- ❌ **Fails**: Syntax errors, test failures, import errors

## Project Structure

```
├── app/                    # Application code
│   ├── configs/           # Configuration files
│   ├── models/            # Data models
│   ├── repositories/      # Data access layer
│   ├── routes/            # API routes
│   ├── schemas/           # Request/response schemas  
│   ├── use_cases/         # Business logic
│   └── utils/             # Utility functions
├── tests/                 # Test files
├── docs/                  # Documentation
├── scripts/               # Development scripts
├── .github/workflows/     # CI/CD configuration
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
├── pyproject.toml        # Tool configuration
└── .flake8              # Linting configuration
```

## Configuration

### Environment Variables
Create a `.env` file:
```
MONGO_URI=mongodb://localhost:27017
```

### Development Tools
- **flake8**: Code linting and style checking
- **black**: Code formatting (127 character line length)
- **isort**: Import sorting and organization
- **pytest**: Test configuration (compatible with unittest)

## Testing

The project uses Python's built-in `unittest` framework:

```bash
# Run all tests
python -m unittest discover tests -v

# Run specific test file
python -m unittest tests.test_login_uc -v

# Run specific test method
python -m unittest tests.test_login_uc.TestLoginUC.test_successful_login -v
```

### Test Structure:
- `tests/test_login_uc.py` - Login use case tests
- `tests/test_password_utils.py` - Password utility tests

## Contributing

1. **Before committing:**
   - Run quality checks: `./scripts/check-quality.sh`
   - Ensure all tests pass
   - Fix any syntax errors

2. **Code style:**
   - Follow PEP 8 guidelines
   - Use black formatter: `black --line-length=127 .`
   - Sort imports: `isort .`

3. **Testing:**
   - Write tests for new features
   - Maintain test coverage
   - Use descriptive test names

## Documentation

- [Development Guide](docs/development-guide.md) - Detailed development setup and practices
- [Password Utility](docs/password_utility.md) - Password hashing and verification guide

## License

[Add your license information here]