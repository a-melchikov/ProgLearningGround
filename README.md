# ProgLearningGround

**ProgLearningGround** is a platform designed to help people learn programming and solve coding challenges.

---

## Tools and Linters Used in the Project

This project adheres to best practices for code quality, testing, and static analysis. Below is a list of the tools and linters integrated into the development process:

### 1. **[Ruff](https://github.com/astral-sh/ruff)**
   - Configured through `ruff.toml`.

### 2. **[Black](https://github.com/psf/black)**

### 3. **[Mypy](https://github.com/python/mypy)**
   - Configured through `mypy.ini`.

### 4. **[Pytest](https://docs.pytest.org/)**

---

## Pre-commit Hooks

To maintain code quality and consistency, **pre-commit** hooks are configured to automatically run the above tools before committing code to the repository.

### Tools Configured in Pre-commit:
- **Ruff**: Lints the codebase.
- **Black**: Formats the code.
- **Mypy**: Performs static type checks.
- **Pytest**: Runs the test suite.
