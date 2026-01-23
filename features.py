"""Compatibility shim for unpickling artifacts trained with `features` module."""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

import pandas as pd
from sklearn.preprocessing import LabelEncoder

from src import config
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
        df = X.copy()
        today = pd.Timestamp.today().normalize()
        if "fl_date" not in df.columns:
            if {"year", "month", "day_of_month"}.issubset(df.columns):
                df["fl_date"] = pd.to_datetime(
                    df[["year", "month", "day_of_month"]].rename(columns={"day_of_month": "day"}),
                    errors="coerce",
                )
            else:
                df["fl_date"] = today
        df["fl_date"] = pd.to_datetime(df["fl_date"], errors="coerce").fillna(today)

        if "crs_dep_time" not in df.columns:
            if {"dep_hour", "sched_minute_of_day"}.issubset(df.columns):
                minutes = df["sched_minute_of_day"] % 60
                df["crs_dep_time"] = (df["dep_hour"] * 100) + minutes
            elif "dep_hour" in df.columns:
                df["crs_dep_time"] = df["dep_hour"] * 100
            else:
                df["crs_dep_time"] = 0
        df["crs_dep_time"] = df["crs_dep_time"].fillna(0)

        if "temp" not in df.columns:
            df["temp"] = 20.0
        if "precip_1h" not in df.columns:
            df["precip_1h"] = 0.0

        if "origin_weather_tavg" not in df.columns:
            df["origin_weather_tavg"] = df["temp"]
        if "dest_weather_tavg" not in df.columns:
            df["dest_weather_tavg"] = df["temp"]
        if "origin_weather_prcp" not in df.columns:
            df["origin_weather_prcp"] = df["precip_1h"]
        if "dest_weather_prcp" not in df.columns:
            df["dest_weather_prcp"] = df["precip_1h"]

        fit_encoders = False
        if self.encoders is None:
            fit_encoders = True
        else:
            for feature in config.CATEGORICAL_FEATURES:
                if feature not in self.encoders:
                    fit_encoders = True
                    break

        features, encoders = feature_engineering_pipeline(df, encoders=self.encoders, fit_encoders=fit_encoders)
        if fit_encoders:
            self.encoders = encoders
        return features

    def fit_transform(self, X: pd.DataFrame, y: Any = None) -> pd.DataFrame:
        self.fit(X, y)
        return self.transform(X)

    def __setstate__(self, state: Dict[str, Any]) -> None:
        self.__dict__.update(state)
        if "encoders" not in self.__dict__:
            self.encoders = None


__all__ = ["FlightFeatureEngineer"] + [name for name in globals() if not name.startswith("_")]
