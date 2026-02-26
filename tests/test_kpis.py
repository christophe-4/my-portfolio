from __future__ import annotations

import pandas as pd

from troel_ops_kit.kpis import compute_avg_daily_demand


def test_compute_avg_daily_demand_keeps_sku_column() -> None:
    demand = pd.DataFrame(
        {
            "date": ["2026-02-20", "2026-02-22"],
            "sku": ["SKU-0001", "SKU-0001"],
            "demand_qty": [10.0, 20.0],
        }
    )

    out = compute_avg_daily_demand(demand, window_days=2)

    assert {"date", "sku", "avg_daily_demand"}.issubset(set(out.columns))
    assert (out["sku"] == "SKU-0001").all()


def test_compute_avg_daily_demand_empty_input() -> None:
    demand = pd.DataFrame(columns=["date", "sku", "demand_qty"])
    out = compute_avg_daily_demand(demand, window_days=28)
    assert list(out.columns) == ["date", "sku", "avg_daily_demand"]
    assert out.empty
