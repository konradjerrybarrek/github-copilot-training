# 🐍 GitHub Copilot Instructions for FastAPI Project

## Project Overview
This is a small RESTful API built with Python and the FastAPI framework. We prioritize clean, modern Python standards and clear separation of concerns.

## Tech Stack & Structure
* **Primary Language:** Python 3.10+
* **Framework:** FastAPI (with Uvicorn).
* **Dependency Manager:** uv (configured via pyproject.toml).
* **Data Models:** Pydantic models for all data validation and serialization.

## Mandatory Coding Guidelines (Copilot Context)
1.  **Asynchronous Code:** All route handlers and I/O-bound functions **must** be defined using `async def` and utilize `await`.
2.  **Type Hints:** All function signatures (parameters and return values) **must** use explicit, descriptive type hints.
3.  **Testing:** Any new endpoint or utility function **must** have a corresponding test in the `tests/` directory using `pytest` and `httpx.AsyncClient`.
4.  **Model Location:** All Pydantic data models **must** be placed in a dedicated `app/models.py` file.
5.  **Return Type:** API endpoints must return standard Python dicts/lists or Pydantic models, not f-strings or raw strings.

## Testing Standards
### Directory Structure
- Unit tests go in `tests/unit/`, integration tests go in `tests/integration/`.
- Shared fixtures (e.g., `app`, `client`) are defined in `tests/conftest.py`.
- Do **not** create test files outside the `tests/` directory.

### Naming Conventions
- Test files: `test_<module>.py` (e.g., `app/main.py` → `tests/unit/test_main.py`).
- Test functions: `test_<target>_<expected_behavior>` (e.g., `test_get_tasks_returns_list`).

### Unit Tests
- Test one function or class in isolation.
- Mock all external/async I/O dependencies using `unittest.mock` or `pytest-mock`.
- Use `pytest.raises` to assert expected exceptions.
- Do **not** spin up the FastAPI app for unit tests.

### Integration Tests
- Use `httpx.AsyncClient` with the FastAPI `app` directly (no live server needed).
- Mark every integration test with both `@pytest.mark.asyncio` and `@pytest.mark.integration`.
- Cover: happy path, validation errors (422), not-found cases (404), and edge cases.
- Assert HTTP status codes, JSON response structure, and Pydantic model conformance.

### Coverage
- Run coverage with: `uv run pytest --cov=app tests/`
- Target **85%+** coverage for any changed module.