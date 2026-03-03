from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field, field_validator


class SalesRow(BaseModel):
    date: date
    sku: str = Field(min_length=1)
    qty: float

    @field_validator("qty")
    @classmethod
    def qty_non_negative(cls, v: float) -> float:
        if v < 0:
            raise ValueError("qty must be >= 0")
        return v


class StockRow(BaseModel):
    snapshot_date: date
    sku: str = Field(min_length=1)
    on_hand_qty: float

    @field_validator("on_hand_qty")
    @classmethod
    def stock_non_negative(cls, v: float) -> float:
        if v < 0:
            raise ValueError("on_hand_qty must be >= 0")
        return v


class CatalogRow(BaseModel):
    sku: str = Field(min_length=1)
    description: str | None = None
    category: str | None = None
    supplier: str | None = None
    unit_cost: float | None = None


class PurchaseOrderRow(BaseModel):
    po_id: str = Field(min_length=1)
    supplier: str | None = None
    sku: str = Field(min_length=1)
    qty_ordered: float
    order_date: date
    expected_date: date
    status: str = "open"

    @field_validator("qty_ordered")
    @classmethod
    def po_qty_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("qty_ordered must be > 0")
        return v
