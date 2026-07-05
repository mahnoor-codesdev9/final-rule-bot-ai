"""Logging helpers for the FastAPI application.

Centralize logger creation so the application has a predictable formatting
and can be configured by deployments. The function is idempotent and safe
to call multiple times during import-time in tests.
"""

from __future__ import annotations

import logging
from logging import StreamHandler, Formatter


def configure_logging(level: int = logging.INFO) -> None:
    """Configure application logging with a stable formatter.

    This avoids the global side-effects of basicConfig and ensures the
    `rulebot` logger uses a single stream handler suitable for containers.
    """
    logger = logging.getLogger("rulebot")

    if logger.handlers:
        # Already configured.
        return

    formatter = Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        "%Y-%m-%dT%H:%M:%S%z",
    )
    handler = StreamHandler()
    handler.setFormatter(formatter)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False


logger = logging.getLogger("rulebot")
