from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from pydantic import BaseModel, ValidationError

from .contracts import CatalogRow, PurchaseOrderRow, SalesRow, StockRow


@dataclass
class ValidationIssue:
    level: str  # "error" | "warning"
    dataset: str
    row: int
    field: str
    message: str


def _validate_rows(df: pd.DataFrame, model: type[BaseModel], dataset: str) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for i, row in enumerate(df.to_dict(orient="records")):
        try:
            model.model_validate(row)
        except ValidationError as e:
            for err in e.errors():
                field = ".".join(str(x) for x in err.get("loc", [])) or "<row>"
                issues.append(
                    ValidationIssue(
                        level="error",
                        dataset=dataset,
                        row=i,
                        field=field,
                        message=err.get("msg", "invalid"),
                    )
                )
    return issues


def validate_sales(df: pd.DataFrame) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if df.duplicated(subset=["date", "sku"]).any():
        dup_idx = df[df.duplicated(subset=["date", "sku"], keep=False)].index.tolist()[:25]
        for i in dup_idx:
            issues.append(ValidationIssue("warning", "sales", int(i), "date,sku", "duplicate key"))
    issues += _validate_rows(df, SalesRow, "sales")
    return issues


def validate_stock(df: pd.DataFrame) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if df.duplicated(subset=["snapshot_date", "sku"]).any():
        dup_idx = df[df.duplicated(subset=["snapshot_date", "sku"], keep=False)].index.tolist()[:25]
        for i in dup_idx:
            issues.append(ValidationIssue("warning", "stock", int(i), "snapshot_date,sku", "duplicate key"))
    issues += _validate_rows(df, StockRow, "stock")
    return issues


def validate_catalog(df: pd.DataFrame) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if df["sku"].isna().any():
        idx = df[df["sku"].isna()].index.tolist()[:25]
        for i in idx:
            issues.append(ValidationIssue("error", "catalog", int(i), "sku", "sku is missing"))
    issues += _validate_rows(df.fillna(value={"sku": ""}), CatalogRow, "catalog")
    return issues


def validate_po(df: pd.DataFrame) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    issues += _validate_rows(df, PurchaseOrderRow, "po")
    bad = df[df["expected_date"] < df["order_date"]]
    for i in bad.index.tolist()[:25]:
        issues.append(ValidationIssue("error", "po", int(i), "expected_date", "expected_date must be >= order_date"))
    return issues


def validate_cross_datasets(
    sales: pd.DataFrame, stock: pd.DataFrame, catalog: pd.DataFrame
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    cat_skus = set(catalog["sku"].astype(str))
    for ds_name, df in [("sales", sales), ("stock", stock)]:
        unknown = df[~df["sku"].astype(str).isin(cat_skus)]
        for i in unknown.index.tolist()[:25]:
            issues.append(ValidationIssue("warning", ds_name, int(i), "sku", "sku not found in catalog"))
    return issues


def issues_to_frame(issues: list[ValidationIssue]) -> pd.DataFrame:
    if not issues:
        return pd.DataFrame(columns=["level", "dataset", "row", "field", "message"])
    return pd.DataFrame([i.__dict__ for i in issues]).sort_values(["level", "dataset", "row"])
