# Core Python For Every Project

## 1. Project Structure
- `src/` for application code
- `tests/` for tests
- `docs/` for notes/design
- `data/sample/` for safe sample data
- `scripts/` for runnable demos

## 2. Dependencies
- Put project dependencies in `pyproject.toml` or `requirements.txt`
- Do not commit `.venv/`
- Know what each package is for

## 3. Data Shapes
- Define what clean input/output objects look like
- Use dataclasses or Pydantic when structure matters

## 4. File Paths
- Use `pathlib.Path`
- Avoid hard-coded local-only paths when possible

## 5. Tests
- Write tests for happy path
- Write tests for failure modes
- Run with `python -m unittest discover -s tests`

## 6. Formatting
- Keep imports at the top
- Constants/rules near top
- Shapes before functions that return them
- Main workflow functions near bottom

## 7. GitHub Hygiene
- Commit source, tests, docs, sample data
- Do not commit `.venv/`, `.idea/`, `__pycache__/`, `.DS_Store`