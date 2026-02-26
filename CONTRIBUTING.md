# Contributing

Thanks for contributing to `TROEL OPS Kit`.

## Setup
```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -e ".[dev]"
```

## Development workflow
1. Create a feature branch.
2. Keep changes small and explainable.
3. Run checks before opening a PR:
```bash
pytest
ruff check .
mypy src
```

## Scope expectations
- Preserve SME-friendly pragmatism.
- Keep rules auditable and deterministic.
- Do not add client data or proprietary datasets.
