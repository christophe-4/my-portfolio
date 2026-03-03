from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class Alert:
    code: str
    severity: str  # info | warning | critical
    sku: str
    message: str
    metric: float | None = None
    asof: date | None = None


Rule = Callable[..., list[Alert]]


def rule_low_coverage(coverage: pd.DataFrame, threshold_days: float = 7.0) -> list[Alert]:
    'Rupture probable: coverage_days < threshold.'
    alerts: list[Alert] = []
    df = coverage.replace([np.inf], np.nan).dropna(subset=["coverage_days"])
    bad = df[df["coverage_days"] < threshold_days].sort_values("coverage_days")
    for _, r in bad.head(50).iterrows():
        alerts.append(
            Alert(
                code="LOW_COVERAGE",
                severity="critical" if r["coverage_days"] < (threshold_days / 2) else "warning",
                sku=str(r["sku"]),
                message=f"Couverture faible ({r['coverage_days']:.1f} jours)",
                metric=float(r["coverage_days"]),
                asof=r["snapshot_date"],
            )
        )
    return alerts


def rule_dead_sku(dormant: pd.DataFrame, lookback_days: int = 60) -> list[Alert]:
    'Référence morte: stock > 0 et 0 vente sur N jours.'
    alerts: list[Alert] = []
    for _, r in dormant.head(50).iterrows():
        alerts.append(
            Alert(
                code="DEAD_SKU",
                severity="warning",
                sku=str(r["sku"]),
                message=f"Aucune vente sur {lookback_days}j avec stock>0",
                metric=float(r["on_hand_qty"]),
                asof=r["snapshot_date"],
            )
        )
    return alerts


def rule_data_quality_issues(issues_df: pd.DataFrame) -> list[Alert]:
    'Data quality: erreurs/warnings issues lors de la validation.'
    alerts: list[Alert] = []
    if issues_df.empty or "level" not in issues_df.columns:
        return alerts
    errs = issues_df[issues_df["level"] == "error"]
    if not errs.empty:
        alerts.append(
            Alert(
                code="DATA_QUALITY",
                severity="critical",
                sku="*",
                message=f"{len(errs)} erreur(s) de validation (voir issues.csv)",
                metric=float(len(errs)),
            )
        )
    return alerts


DEFAULT_RULES: dict[str, Rule] = {
    "low_coverage": rule_low_coverage,
    "dead_sku": rule_dead_sku,
    "data_quality": rule_data_quality_issues,
}


def alerts_to_frame(alerts: list[Alert]) -> pd.DataFrame:
    if not alerts:
        return pd.DataFrame(columns=["code", "severity", "sku", "message", "metric", "asof"])
    return pd.DataFrame([a.__dict__ for a in alerts]).sort_values(
        ["severity", "code", "metric"], ascending=[True, True, True]
    )
