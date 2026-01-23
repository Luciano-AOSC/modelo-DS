"""Compatibility shim for unpickling models trained with `modeling` module."""

from __future__ import annotations

from typing import Any

import xgboost as xgb

from src import modeling as _modeling


class OutOfCoreXGBModel(xgb.XGBClassifier):
    """Legacy wrapper preserved to satisfy pickle imports."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def __setstate__(self, state: dict) -> None:
        if isinstance(state, dict):
            self.__dict__.update(state)
        if not hasattr(self, "objective"):
            self.objective = "binary:logistic"
        if not hasattr(self, "verbosity"):
            self.verbosity = 0


__all__ = ["OutOfCoreXGBModel"] + [name for name in dir(_modeling) if not name.startswith("_")]

for name in __all__:
    if name == "OutOfCoreXGBModel":
        globals()[name] = OutOfCoreXGBModel
    else:
        globals()[name] = getattr(_modeling, name)
