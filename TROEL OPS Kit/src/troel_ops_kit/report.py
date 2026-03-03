from __future__ import annotations

import pathlib
from datetime import date

import pandas as pd
from jinja2 import Environment, PackageLoader, select_autoescape


def render_markdown(
    coverage: pd.DataFrame,
    abc: pd.DataFrame,
    alerts: pd.DataFrame,
    out_path: str | pathlib.Path,
    title: str = "TROEL OPS Kit Report",
) -> pathlib.Path:
    env = Environment(
        loader=PackageLoader("troel_ops_kit", "templates"),
        autoescape=select_autoescape(enabled_extensions=("html", "xml")),
    )
    tmpl = env.get_template("report.md.j2")

    low_cov = coverage.replace([float("inf")], pd.NA).dropna(subset=["coverage_days"]).head(10)
    top_a = abc[abc["abc"] == "A"].head(10)
    alert_top = alerts.head(15)

    md = tmpl.render(
        title=title,
        generated_on=date.today().isoformat(),
        low_coverage=low_cov.to_dict(orient="records"),
        top_a=top_a.to_dict(orient="records"),
        alerts=alert_top.to_dict(orient="records"),
        totals={
            "skus_stock": int(coverage["sku"].nunique()),
            "skus_sales": int(abc["sku"].nunique()),
            "alerts": int(len(alerts)),
        },
    )

    out_path = pathlib.Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    return out_path


def markdown_to_pdf(md_path: str | pathlib.Path, pdf_path: str | pathlib.Path) -> pathlib.Path:
    'Convert report.md to a basic PDF using WeasyPrint (optional extra).'
    from weasyprint import HTML  # optional dependency

    md = pathlib.Path(md_path).read_text(encoding="utf-8")
    html = (
        "<html><body><pre style='font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "
        "Liberation Mono, Courier New, monospace; font-size: 11px'>"
        + md
        + "</pre></body></html>"
    )
    pdf_path = pathlib.Path(pdf_path)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html).write_pdf(str(pdf_path))
    return pdf_path
