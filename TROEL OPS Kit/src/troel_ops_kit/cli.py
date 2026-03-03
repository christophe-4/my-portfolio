from __future__ import annotations

import json
import pathlib

import typer
from rich.console import Console
from rich.table import Table

from .demo import generate_demo
from .logging_config import configure_logging
from .pipeline import run as run_pipeline
from .report import markdown_to_pdf

app = typer.Typer(add_completion=False, help="TROEL OPS Kit - Supply Chain KPI & Alerts Toolkit.")
demo_app = typer.Typer(help="Demo dataset utilities.")
app.add_typer(demo_app, name="demo")

console = Console()


@app.callback()
def main(
    log_level: str = typer.Option("INFO", help="Logging level: DEBUG|INFO|WARNING|ERROR"),
) -> None:
    "Global CLI options."
    configure_logging(log_level)


@demo_app.command("generate")
def demo_generate(out: str = typer.Option("./data/demo", help="Output folder for demo CSV files")) -> None:
    "Generate synthetic datasets (sales/stock/catalog) as CSV."
    generate_demo(out)
    console.print(f"[green]OK[/green] Demo data generated in: {out}")


@app.command()
def run(
    sales: str = typer.Option(..., help="Path to sales CSV/XLSX"),
    stock: str = typer.Option(..., help="Path to stock CSV/XLSX"),
    catalog: str = typer.Option(..., help="Path to catalog CSV/XLSX"),
    out: str = typer.Option("./out", help="Output folder"),
    mapping: str | None = typer.Option(None, help="Optional JSON mapping file for columns"),
) -> None:
    "End-to-end run: ingest + validate + KPIs + alerts + report.md."
    mapping_obj = None
    if mapping:
        mapping_obj = json.loads(pathlib.Path(mapping).read_text(encoding="utf-8"))

    res = run_pipeline(sales, stock, catalog, out_dir=out, mapping=mapping_obj)
    console.print(f"[green]OK[/green] Report: {res.report_path}")

    t = Table(title="Top alerts (demo)")
    for col in ["severity", "code", "sku", "message", "metric"]:
        t.add_column(col)
    for _, r in res.alerts.head(10).iterrows():
        t.add_row(
            str(r.get("severity", "")),
            str(r.get("code", "")),
            str(r.get("sku", "")),
            str(r.get("message", "")),
            str(r.get("metric", "")),
        )
    console.print(t)


@app.command()
def report(
    in_dir: str = typer.Option("./out", help="Folder containing report.md"),
    format: str = typer.Option("md", help="md|pdf"),
) -> None:
    "Convert report.md to PDF (requires extra: troel-ops-kit[pdf])."
    in_path = pathlib.Path(in_dir) / "report.md"
    if not in_path.exists():
        raise FileNotFoundError(str(in_path))

    if format.lower() == "md":
        console.print(str(in_path))
        raise typer.Exit(code=0)

    if format.lower() == "pdf":
        pdf_path = pathlib.Path(in_dir) / "report.pdf"
        markdown_to_pdf(in_path, pdf_path)
        console.print(f"[green]OK[/green] PDF generated: {pdf_path}")
        raise typer.Exit(code=0)

    raise typer.BadParameter("format must be 'md' or 'pdf'")
