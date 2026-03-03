import pathlib

from troel_ops_kit.demo import generate_demo
from troel_ops_kit.pipeline import run


def test_end_to_end(tmp_path: pathlib.Path):
    data_dir = tmp_path / "data"
    out_dir = tmp_path / "out"
    generate_demo(data_dir, n_skus=50, days=90, seed=1)

    res = run(
        sales_path=str(data_dir / "sales.csv"),
        stock_path=str(data_dir / "stock.csv"),
        catalog_path=str(data_dir / "catalog.csv"),
        out_dir=str(out_dir),
    )

    assert (out_dir / "kpi_coverage.csv").exists()
    assert (out_dir / "alerts.csv").exists()
    assert (out_dir / "report.md").exists()
    assert len(res.coverage) > 0
