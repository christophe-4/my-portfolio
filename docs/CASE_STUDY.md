# Case Study (Synthetic) - Preventing Stockouts With Explainable Rules

## Context
A mid-size distributor runs weekly exports from ERP and wants a lightweight way to detect:
- imminent stockout risks,
- dormant inventory tying up cash,
- priority SKUs by value impact.

## Input data (synthetic)
- `sales.csv`: daily sales by SKU
- `stock.csv`: stock snapshot by SKU
- `catalog.csv`: product metadata and unit cost

## Approach
1. Validate data quality (types, duplicates, missing/unknown SKUs)
2. Compute KPIs:
- coverage days (`on_hand_qty / avg_daily_demand`)
- dormant stock (no sales in lookback window)
- ABC class from consumption value
3. Apply explainable alerts:
- `LOW_COVERAGE` if coverage < threshold
- `DEAD_SKU` if stock > 0 and no recent sales
- `DATA_QUALITY` if validation errors exist

## Typical output
- Action list for buyers/planners from `alerts.csv`
- Portfolio-ready summary from `report.md`
- Traceable issues in `issues.csv`

## Why this is portfolio-relevant
- Mirrors real operations pain points
- Shows pragmatic automation and code quality
- Keeps governance simple (auditable rules, no black box)
