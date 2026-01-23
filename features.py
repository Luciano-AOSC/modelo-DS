"""Compatibility shim for unpickling artifacts trained with `features` module."""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

import pandas as pd
from sklearn.preprocessing import LabelEncoder

from src.features import *  # noqa: F403
from src.features import feature_engineering_pipeline


class FlightFeatureEngineer:
    """Legacy feature engineering wrapper preserved for pickle compatibility."""

    def __init__(self, encoders: Optional[Dict[str, LabelEncoder]] = None) -> None:
        self.encoders = encoders

    def fit(self, X: pd.DataFrame, y: Any = None) -> "FlightFeatureEngineer":
        features, encoders = feature_engineering_pipeline(X, encoders=self.encoders, fit_encoders=True)
        self.encoders = encoders
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        features, _ = feature_engineering_pipeline(X, encoders=self.encoders, fit_encoders=False)
        return features

    def fit_transform(self, X: pd.DataFrame, y: Any = None) -> pd.DataFrame:
        self.fit(X, y)
        return self.transform(X)

    def __setstate__(self, state: Dict[str, Any]) -> None:
        self.__dict__.update(state)
        if "encoders" not in self.__dict__:
            self.encoders = None


__all__ = ["FlightFeatureEngineer"] + [name for name in globals() if not name.startswith("_")]
