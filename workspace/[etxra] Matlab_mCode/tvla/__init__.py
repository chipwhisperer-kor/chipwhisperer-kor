"""
TVLA (fixed vs random) package.

Public entry points (keep this list small — KISS):

    from tvla import h5_on_mem, tvla_from_arrays

- ``h5_on_mem`` / math / memory rules: implemented in ``h5_on_mem.py``
  (that module is SSOT for the algorithm).
- Batch CLI: ``python -m tvla.run_tvla`` (SSOT for paths and loop options).
"""

from .h5_on_mem import h5_on_mem, tvla_from_arrays

__all__ = ["h5_on_mem", "tvla_from_arrays"]
