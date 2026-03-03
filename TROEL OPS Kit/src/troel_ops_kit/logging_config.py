from __future__ import annotations

import logging


def configure_logging(level: str = "INFO") -> None:
    """
    Configure console logging once for CLI execution.

    The message body is intentionally key=value friendly so logs stay readable
    in terminals and in CI logs without external dependencies.
    """
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
