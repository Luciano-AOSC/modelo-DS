"""
Lógica de negocio para la API.
"""

from functools import lru_cache
from typing import Any, Dict, Tuple
import json

import joblib
import pandas as pd
from fastapi import HTTPException

from .. import config
from ..features import get_feature_columns

REQUIRED_COLUMNS = [
    "op_unique_carrier",
    "origin",
    "dest",
    "year",
    "month",
    "day_of_week",
    "day_of_month",
    "dep_hour",
    "sched_minute_of_day",
    "distance",
    "temp",
    "wind_spd",
    "precip_1h",
    "climate_severity_idx",
    "dist_met_km",
    "latitude",
    "longitude",
]


# Tuple[Any, Any, Dict[str, Any]] = (modelo, feature_engineer, metadata).
# - Any: objeto cargado con joblib (modelo o pipeline de features).
# - Dict[str, Any]: metadata del modelo.
@lru_cache(maxsize=1)
def load_artifacts() -> Tuple[Any, Any, Dict[str, Any]]:
    """
    Carga modelo, feature engineer y metadata desde disco.

    Retorna:
        (model, feature_engineer, metadata)
    """
    model = joblib.load(config.MODEL_PATH)
    feature_engineer = joblib.load(config.FEATURE_ENGINEER_PATH)
    with open(config.METADATA_PATH, "r", encoding="utf-8") as file:
        metadata = json.load(file)
    return model, feature_engineer, metadata


def validate_payload(df: pd.DataFrame) -> None:
    """
    Valida que el payload tenga todas las columnas y sin nulos.

    Args:
        df: DataFrame con un solo vuelo.
    """
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise HTTPException(
            status_code=400,
            detail=f"Faltan columnas requeridas: {', '.join(missing_columns)}",
        )

    null_columns = df[REQUIRED_COLUMNS].columns[df[REQUIRED_COLUMNS].isnull().any()].tolist()
    if null_columns:
        raise HTTPException(
            status_code=400,
            detail=f"Columnas con valores nulos: {', '.join(null_columns)}",
        )


def build_features(
    df: pd.DataFrame,
    feature_engineer: Any,
    feature_names: list,
) -> pd.DataFrame:
    """
    Ejecuta el pipeline de features para inferencia.

    Args:
        df: DataFrame con el vuelo.
        feature_engineer: pipeline entrenado para construir las features.
        feature_names: lista ordenada de columnas esperadas por el modelo.

    Returns:
        DataFrame listo para escalar y predecir.
    """
    if not hasattr(feature_engineer, "transform"):
        raise HTTPException(
            status_code=500,
            detail="El feature engineer no soporta transform().",
        )

    transformed = feature_engineer.transform(df)
    if isinstance(transformed, pd.DataFrame):
        return transformed
    return pd.DataFrame(transformed, columns=feature_names)


def sanitize_payload(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia valores fuera de rango antes de generar features.
    """
    df_clean = df.copy()
    today = pd.Timestamp.today().normalize()
    if "fl_date" not in df_clean.columns:
        if {"year", "month", "day_of_month"}.issubset(df_clean.columns):
            df_clean["fl_date"] = pd.to_datetime(
                df_clean[["year", "month", "day_of_month"]].rename(
                    columns={"day_of_month": "day"}
                ),
                errors="coerce",
            )
        else:
            df_clean["fl_date"] = today
    df_clean["fl_date"] = pd.to_datetime(df_clean["fl_date"], errors="coerce").fillna(today)

    if "crs_dep_time" not in df_clean.columns:
        if {"dep_hour", "sched_minute_of_day"}.issubset(df_clean.columns):
            minutes = df_clean["sched_minute_of_day"] % 60
            df_clean["crs_dep_time"] = (df_clean["dep_hour"] * 100) + minutes
        elif "dep_hour" in df_clean.columns:
            df_clean["crs_dep_time"] = df_clean["dep_hour"] * 100
        else:
            df_clean["crs_dep_time"] = 0
    df_clean["crs_dep_time"] = df_clean["crs_dep_time"].fillna(0)
    default_values = {
        "temp": 20.0,
        "wind_spd": 5.0,
        "precip_1h": 0.0,
        "climate_severity_idx": 0.0,
        "dist_met_km": 10.0,
        "latitude": 40.0,
        "longitude": -74.0,
    }
    for key, value in default_values.items():
        if key not in df_clean.columns:
            df_clean[key] = value
        else:
            df_clean[key] = df_clean[key].fillna(value)
    if "precip_1h" in df_clean.columns:
        df_clean["precip_1h"] = df_clean["precip_1h"].clip(lower=0)
    return df_clean


def predict_from_payload(df: pd.DataFrame) -> Tuple[int, float]:
    """
    Calcula predicción y probabilidad para un solo vuelo.

    Args:
        df: DataFrame con un solo vuelo.

    Returns:
        (prediction, probability)
    """
    df = sanitize_payload(df)
    validate_payload(df)
    model, feature_engineer, metadata = load_artifacts()
    feature_columns = metadata.get("feature_names", get_feature_columns())
    df_features = build_features(df, feature_engineer, feature_columns)
    missing_feature_columns = [col for col in feature_columns if col not in df_features.columns]
    if missing_feature_columns:
        raise HTTPException(
            status_code=400,
            detail=f"No se pudieron construir las features: {', '.join(missing_feature_columns)}",
        )

    x_features = df_features[feature_columns].copy().fillna(0)
    probability = float(model.predict_proba(x_features)[0, 1])
    threshold = metadata.get("threshold", config.CLASSIFICATION_THRESHOLD)
    prediction = int(probability >= threshold)

    return prediction, probability
