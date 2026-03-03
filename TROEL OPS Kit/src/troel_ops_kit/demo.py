from __future__ import annotations

import pathlib
from datetime import date, timedelta

import numpy as np
import pandas as pd


def generate_demo(out_dir: str | pathlib.Path, n_skus: int = 200, days: int = 120, seed: int = 7) -> None:
    'Generate synthetic datasets: sales.csv, stock.csv, catalog.csv.'
    rng = np.random.default_rng(seed)
    out_dir = pathlib.Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    skus = [f"SKU-{i:04d}" for i in range(1, n_skus + 1)]
    categories = ["AUDIO", "CABLE", "POWER", "DISPLAY", "CONSUMABLE"]
    suppliers = ["SUP-ALPHA", "SUP-BETA", "SUP-GAMMA"]

    catalog = pd.DataFrame(
        {
            "sku": skus,
            "description": [f"Product {s}" for s in skus],
            "category": rng.choice(categories, size=n_skus, replace=True),
            "supplier": rng.choice(suppliers, size=n_skus, replace=True),
            "unit_cost": np.round(rng.uniform(1.0, 120.0, size=n_skus), 2),
        }
    )
    catalog.to_csv(out_dir / "catalog.csv", index=False)

    end = date.today()
    start = end - timedelta(days=days - 1)
    all_days = [start + timedelta(days=i) for i in range(days)]

    rows = []
    for d in all_days:
        active = rng.choice(skus, size=max(1, int(n_skus * 0.25)), replace=False)
        for sku in active:
            base = int(rng.poisson(lam=float(rng.uniform(0.2, 3.0))))
            if base == 0:
                continue
            if rng.random() < 0.02:
                base *= int(rng.integers(5, 12))
            rows.append((d.isoformat(), sku, float(base)))

    sales = pd.DataFrame(rows, columns=["date", "sku", "qty"])
    sales.to_csv(out_dir / "sales.csv", index=False)

    stock = pd.DataFrame(
        {
            "snapshot_date": [end.isoformat()] * n_skus,
            "sku": skus,
            "on_hand_qty": np.round(rng.uniform(0, 250, size=n_skus), 0),
        }
    )

    if len(skus) >= 5:
        for s in skus[:3]:
            stock.loc[stock["sku"] == s, "on_hand_qty"] = 1

        dormant_sku = skus[4]
        sales2 = sales.copy()
        sales2["date_dt"] = pd.to_datetime(sales2["date"]).dt.date
        sales2 = sales2[~((sales2["sku"] == dormant_sku) & (sales2["date_dt"] >= end - timedelta(days=60)))]
        sales2.drop(columns=["date_dt"]).to_csv(out_dir / "sales.csv", index=False)

    stock.to_csv(out_dir / "stock.csv", index=False)
