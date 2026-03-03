from __future__ import annotations

from collections.abc import Mapping
import pathlib

import pandas as pd


def read_tabular(path: str | pathlib.Path) -> pd.DataFrame:
    'Read CSV or Excel into a DataFrame.'
    p = pathlib.Path(path)
    if not p.exists():
        raise FileNotFoundError(str(p))

    if p.suffix.lower() in {".csv", ".txt"}:
        return pd.read_csv(p)
    if p.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(p, engine="openpyxl")
    raise ValueError(f"Unsupported file type: {p.suffix}")


def apply_mapping(df: pd.DataFrame, mapping: Mapping[str, str] | None) -> pd.DataFrame:
    '''
    Rename columns using a mapping dict {expected_name: actual_column_in_file}.
    Example: {"snapshot_date": "Date", "on_hand_qty": "Stock"}.
    '''
    if not mapping:
        return df
    inverse = {actual: expected for expected, actual in mapping.items()}
    return df.rename(columns=inverse)


def ensure_columns(df: pd.DataFrame, required: list[str], df_name: str) -> None:
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"{df_name}: missing required columns: {missing}")


def coerce_dates(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce").dt.date
    return df
