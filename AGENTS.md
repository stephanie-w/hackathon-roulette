# AGENTS.md - Project Guide for AI Assistants

## Project Structure

```
.
├── src/hackathon_roulette/          # Source code (PEP 420 compliant)
│   ├── __init__.py        # Package initialization
│   ├── __about__.py       # Version management (used by hatch)
│   ├── example.py         # Example module
│   └── main.py           # CLI entry point
├── tests/                 # Test directory
│   └── test_example.py   # Test suite for example module
├── pyproject.toml        # Main configuration file
├── Makefile              # Primary Makefile with common commands
├── Makefile.dev          # Development-specific commands
├── Makefile.ci           # CI/CD and release commands
├── .pre-commit-config.yaml # Git hooks configuration
└── README.md             # Project documentation
```

## Development Commands

### Core Commands (Makefile)

- `make install` - Install package in development mode
- `make install-dev` - Install with development dependencies
- `make lint` - Run ruff linting
- `make format` - Format code with ruff
- `make typecheck` - Run mypy type checking
- `make test` - Run tests with pytest
- `make test-cov` - Run tests with coverage report
- `make clean` - Clean build artifacts and caches
- `make build` - Build package
- `make publish` - Publish to private artifactory

### Development Commands (Makefile.dev)

- `make pre-commit` - Run pre-commit on all files
- `make pre-commit-install` - Install pre-commit hooks
- `make watch` - Watch for file changes and run tests
- `make watch-tests` - Watch test files and run on changes
- `make docs` - Build documentation
- `make docs-serve` - Serve documentation locally

## Code Quality Standards

### Linting & Formatting (ruff)

- **Line length**: 88 characters
- **Quote style**: Double quotes
- **Import ordering**: isort with `known-first-party = ["hackathon_roulette"]`
- **Rules enabled**: E, W, F, I, B, C4, UP, YTT, RUF
- **Rules ignored**: B008, B905, E501, F401 (for **init**.py), RUF012

### Type Checking (mypy)

- **Python version**: 3.13
- **Strict mode enabled**:
  - `disallow_untyped_defs = true`
  - `disallow_incomplete_defs = true`
  - `disallow_untyped_decorators = true`
  - `no_implicit_optional = true`
- **Test exemptions**: Tests have `disallow_untyped_defs = false`

### Testing (pytest)

- **Test directory**: `tests/`
- **Test markers**: `slow`, `integration`, `unit`
- **Coverage minimum**: 72%
- **Test organization**: By function (e.g., `TestValidateEmail`, `TestValidatePhone`)

## Implementation Patterns

### Module Structure

```python
"""Module docstring with description."""

from datetime import datetime
import re
from typing import Optional


def function_name(param: type) -> return_type:
    """Function docstring in Google style.

    Args:
        param: Parameter description

    Returns:
        Return value description

    Raises:
        ValueError: When input validation fails

    Examples:
        >>> function_name("example")
        "result"
    """
    # Implementation
```

### Error Handling

- Use `ValueError` for input validation errors
- Provide descriptive error messages
- Validate inputs at function boundaries

### Test Structure

```python
"""Tests for module."""

import pytest
from hackathon_roulette.module import function_name


class TestFunctionName:
    """Tests for function_name function."""

    def test_function_name_valid(self) -> None:
        assert function_name("valid") is True

    def test_function_name_invalid(self) -> None:
        with pytest.raises(ValueError, match="error message"):
            function_name("invalid")
```

## Package Configuration

### Dependencies

- **Production**: None (pure Python package)
- **Development**: pytest, ruff, mypy, pre-commit, coverage
- **Documentation**: mkdocs, mkdocs-material

### Build System

- **Builder**: hatchling
- **Version management**: Single-source via `src/hackathon_roulette/__about__.py`
- **Package structure**: src-layout (PEP 420)

## Workflow for AI Assistants

### When Adding New Features

1. **Understand existing patterns** - Review similar functions in `example.py`
2. **Add type hints** - All functions must have complete type annotations
3. **Write comprehensive docstrings** - Use Google style with examples
4. **Add tests** - Create test class in `tests/test_example.py`
5. **Run quality checks**:

   ```bash
   make lint
   make format
   make typecheck
   make test-cov
   ```

### When Modifying Existing Code

1. **Maintain type hints** - Ensure all changes preserve type safety
2. **Update tests** - Modify existing tests or add new ones
3. **Preserve formatting** - Run `make format` after changes
4. **Verify coverage** - Ensure coverage remains ≥72%

## Quality Assurance Checklist

Before considering work complete:

- [ ] All functions have type hints and docstrings
- [ ] Tests pass (`make test`)
- [ ] Coverage ≥72% (`make test-cov`)
- [ ] Linting passes (`make lint`)
- [ ] Formatting applied (`make format`)
- [ ] Type checking passes (`make typecheck`)
- [ ] No external dependencies added (unless explicitly requested)

## Notes for AI Agents

- This is a **template/boilerplate** project - focus on patterns not specific functionality
- Keep dependencies **lightweight** - prefer Python standard library
- Follow **existing conventions** - don't introduce new patterns without reason
- **Test organization**: By function, not by file
- **Error handling**: Raise exceptions with descriptive messages
- **Documentation**: Include examples in docstrings
