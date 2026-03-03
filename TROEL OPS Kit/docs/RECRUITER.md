# Recruiter Quick Read - TROEL OPS Kit

## What this demonstrates
`TROEL OPS Kit` is a compact OSS portfolio project showing practical supply chain data automation.

- Turns flat CSV/XLSX exports into a repeatable CLI workflow
- Applies explicit validation and cross-dataset checks
- Produces explainable KPIs and rule-based alerts
- Generates recruiter-readable outputs (`alerts.csv`, `report.md`)

## Why it matters in operations
- Faster identification of stockout risk and dead stock
- Transparent logic that operations teams can audit
- Reusable workflow that can be adapted to SME contexts

## Tech profile signals
- Python packaging (`pyproject.toml`, editable install)
- Testable architecture (`pytest` end-to-end)
- CI-ready repository (`.github/workflows/ci.yml`)
- Practical CLI UX (`typer`, `rich`, logging)

## 60-second run
```bash
pip install -e ".[dev]"
troel-ops demo generate --out ./data/demo
troel-ops run --sales ./data/demo/sales.csv --stock ./data/demo/stock.csv --catalog ./data/demo/catalog.csv --out ./out
```

## Constraints respected
- Synthetic data only (portfolio safe)
- No proprietary client logic
- Explainable rules, not AI magic
