from __future__ import annotations

from datetime import date, timedelta

import numpy as np
import pandas as pd


def compute_daily_demand(sales: pd.DataFrame) -> pd.DataFrame:
    'Returns demand per day and sku.'
    df = sales.copy()
    df["date"] = pd.to_datetime(df["date"]).dt.date
    out = df.groupby(["date", "sku"], as_index=False).agg(demand_qty=("qty", "sum"))
    return out


def compute_avg_daily_demand(demand: pd.DataFrame, window_days: int = 28) -> pd.DataFrame:
    'For each sku, compute rolling average demand/day.'
    if demand.empty:
        return pd.DataFrame(columns=["date", "sku", "avg_daily_demand"])

    df = demand.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["sku", "date"])

    per_sku: list[pd.DataFrame] = []
    for sku, g in df.groupby("sku", sort=False):
        series = g[["date", "demand_qty"]].set_index("date").asfreq("D", fill_value=0.0)
        series["avg_daily_demand"] = series["demand_qty"].rolling(window_days, min_periods=1).mean()
        series = series.reset_index()
        series["date"] = series["date"].dt.date
        series["sku"] = sku
        per_sku.append(series[["date", "sku", "avg_daily_demand"]])

    return pd.concat(per_sku, ignore_index=True)


def compute_coverage_days(stock: pd.DataFrame, avg_demand: pd.DataFrame, asof: date | None = None) -> pd.DataFrame:
    'coverage_days = on_hand_qty / avg_daily_demand.'
    st = stock.copy()
    st["snapshot_date"] = pd.to_datetime(st["snapshot_date"]).dt.date

    if asof is None:
        asof = st["snapshot_date"].max()

    st_asof = st[st["snapshot_date"] == asof].copy()
    ad_asof = avg_demand[avg_demand["date"] == asof].copy()

    df = st_asof.merge(ad_asof, how="left", on="sku")
    df["avg_daily_demand"] = df["avg_daily_demand"].fillna(0.0)
    df["coverage_days"] = np.where(df["avg_daily_demand"] > 0, df["on_hand_qty"] / df["avg_daily_demand"], np.inf)
    df = df[["snapshot_date", "sku", "on_hand_qty", "avg_daily_demand", "coverage_days"]]
    return df.sort_values("coverage_days", ascending=True)


def compute_dormant_stock(sales: pd.DataFrame, stock: pd.DataFrame, lookback_days: int = 60) -> pd.DataFrame:
    'Dormant = stock > 0 and no sales in lookback window.'
    asof = pd.to_datetime(stock["snapshot_date"]).dt.date.max()
    start = asof - timedelta(days=lookback_days)

    s = sales.copy()
    s["date"] = pd.to_datetime(s["date"]).dt.date
    recent = (
        s[(s["date"] >= start) & (s["date"] <= asof)]
        .groupby("sku", as_index=False)
        .agg(sales_lookback_qty=("qty", "sum"))
    )

    st = stock[stock["snapshot_date"] == asof].copy()
    out = st.merge(recent, how="left", on="sku")
    out["sales_lookback_qty"] = out["sales_lookback_qty"].fillna(0.0)
    out = out[(out["on_hand_qty"] > 0) & (out["sales_lookback_qty"] == 0)]
    return out[["snapshot_date", "sku", "on_hand_qty", "sales_lookback_qty"]].sort_values("on_hand_qty", ascending=False)


def compute_abc(sales: pd.DataFrame, catalog: pd.DataFrame) -> pd.DataFrame:
    'ABC basé sur la valeur de consommation (qty * unit_cost) sur toute la période.'
    s = sales.copy().groupby("sku", as_index=False).agg(total_qty=("qty", "sum"))
    c = catalog.copy()
    if "unit_cost" not in c.columns:
        c["unit_cost"] = np.nan

    df = s.merge(c[["sku", "unit_cost", "category", "supplier", "description"]], how="left", on="sku")
    df["unit_cost"] = pd.to_numeric(df["unit_cost"], errors="coerce")
    df["consumption_value"] = np.where(df["unit_cost"].notna(), df["total_qty"] * df["unit_cost"], df["total_qty"])
    df = df.sort_values("consumption_value", ascending=False).reset_index(drop=True)

    total = df["consumption_value"].sum()
    df["cum_pct"] = df["consumption_value"].cumsum() / (total if total else 1.0)

    def abc_bucket(p: float) -> str:
        if p <= 0.80:
            return "A"
        if p <= 0.95:
            return "B"
        return "C"

    df["abc"] = df["cum_pct"].apply(abc_bucket)
    return df[["sku", "total_qty", "unit_cost", "consumption_value", "cum_pct", "abc", "category", "supplier", "description"]]
