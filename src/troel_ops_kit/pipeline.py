from __future__ import annotations

import logging
import pathlib
from collections.abc import Mapping
from dataclasses import dataclass

import pandas as pd

from .alerts import DEFAULT_RULES, alerts_to_frame
from .io import apply_mapping, coerce_dates, ensure_columns, read_tabular
from .kpis import (
    compute_abc,
    compute_avg_daily_demand,
    compute_coverage_days,
    compute_daily_demand,
    compute_dormant_stock,
)
from .report import render_markdown
from .validate import (
    issues_to_frame,
    validate_catalog,
    validate_cross_datasets,
    validate_sales,
    validate_stock,
)

logger = logging.getLogger(__name__)


@dataclass
class RunResult:
    coverage: pd.DataFrame
    abc: pd.DataFrame
    dormant: pd.DataFrame
    issues: pd.DataFrame
    alerts: pd.DataFrame
    report_path: pathlib.Path


def run(
    sales_path: str,
    stock_path: str,
    catalog_path: str,
    out_dir: str,
    mapping: Mapping[str, Mapping[str, str]] | None = None,
) -> RunResult:
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    logger.info("event=start_pipeline out_dir=%s", out)

    mapping = mapping or {}
    sales_map = mapping.get("sales")
    stock_map = mapping.get("stock")
    catalog_map = mapping.get("catalog")

    sales = apply_mapping(read_tabular(sales_path), sales_map)
    stock = apply_mapping(read_tabular(stock_path), stock_map)
    catalog = apply_mapping(read_tabular(catalog_path), catalog_map)
    logger.info(
        "event=ingest sales_rows=%s stock_rows=%s catalog_rows=%s",
        len(sales),
        len(stock),
        len(catalog),
    )

    ensure_columns(sales, ["date", "sku", "qty"], "sales")
    ensure_columns(stock, ["snapshot_date", "sku", "on_hand_qty"], "stock")
    ensure_columns(catalog, ["sku"], "catalog")

    sales = coerce_dates(sales, ["date"])
    stock = coerce_dates(stock, ["snapshot_date"])

    issues = []
    issues += validate_sales(sales)
    issues += validate_stock(stock)
    issues += validate_catalog(catalog)
    issues += validate_cross_datasets(sales, stock, catalog)
    issues_df = issues_to_frame(issues)
    issues_df.to_csv(out / "issues.csv", index=False)
    logger.info("event=validate issues=%s", len(issues_df))

    demand = compute_daily_demand(sales)
    avg = compute_avg_daily_demand(demand, window_days=28)
    coverage = compute_coverage_days(stock, avg)
    dormant = compute_dormant_stock(sales, stock, lookback_days=60)
    abc = compute_abc(sales, catalog)

    coverage.to_csv(out / "kpi_coverage.csv", index=False)
    dormant.to_csv(out / "kpi_dormant.csv", index=False)
    abc.to_csv(out / "kpi_abc.csv", index=False)

    alerts = []
    alerts += DEFAULT_RULES["low_coverage"](coverage, threshold_days=7.0)
    alerts += DEFAULT_RULES["dead_sku"](dormant, lookback_days=60)
    alerts += DEFAULT_RULES["data_quality"](issues_df)

    alerts_df = alerts_to_frame(alerts)
    alerts_df.to_csv(out / "alerts.csv", index=False)
    logger.info("event=alerts total_alerts=%s", len(alerts_df))

    report_path = render_markdown(coverage, abc, alerts_df, out / "report.md", title="TROEL OPS Kit Report")
    logger.info("event=report_written path=%s", report_path)

    return RunResult(
        coverage=coverage,
        abc=abc,
        dormant=dormant,
        issues=issues_df,
        alerts=alerts_df,
        report_path=report_path,
    )
