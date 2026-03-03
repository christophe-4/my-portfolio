# Architecture - TROEL OPS Kit

## Flow
```text
sales.csv + stock.csv + catalog.csv
                |
                v
        io.read_tabular / mapping
                |
                v
      validate.* (contracts + checks)
                |
                v
          kpis.* computations
                |
                v
       alerts.* business rules
                |
                v
  report.render_markdown -> report.md
```

## Modules
- `io.py`: read CSV/XLSX, apply column mapping, coerce dates
- `contracts.py`: row contracts via Pydantic
- `validate.py`: dataset validation + cross-dataset consistency checks
- `kpis.py`: demand, coverage, dormant stock, ABC classification
- `alerts.py`: explainable threshold rules and alert normalization
- `report.py`: Markdown report rendering (+ optional PDF export)
- `pipeline.py`: orchestration with file outputs + structured-ish logging
- `cli.py`: Typer commands (`demo`, `run`, `report`)

## Design principles
- Keep it small and inspectable
- Prefer explicit rules over opaque models
- Optimize for maintainability in SME contexts
- Remain platform-friendly (Linux/macOS/Windows)
