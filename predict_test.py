import importlib.util
import json
from pathlib import Path

import joblib


def load_module(module_name: str, module_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"No se pudo cargar el módulo {module_name} desde {module_path}.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    project_root = Path(__file__).resolve().parent
    config_module = load_module("config", project_root / "src" / "config.py")
    features_module = load_module("features", project_root / "src" / "features.py")

    model_path = Path(config_module.MODEL_PATH)
    feature_engineer_path = Path(config_module.FEATURE_ENGINEER_PATH)

    try:
        with open(model_path, "rb") as model_file:
            model = joblib.load(model_file)
    except ModuleNotFoundError as exc:
        missing = getattr(exc, "name", "dependencias del modelo")
        raise SystemExit(
            "Falta instalar dependencias del modelo. "
            f"Módulo faltante: {missing}. "
            "Ejecuta: pip install -r requirements.txt "
            "y si sigue fallando instala: pip install xgboost lightgbm"
        ) from exc

    with open(feature_engineer_path, "rb") as fe_file:
        feature_engineer = joblib.load(fe_file)

    input_payload = {
        "aerolinea": "AA",
        "origen": "JFK",
        "destino": "LAX",
        "fecha_partida": "2025-03-15T14:30:00",
        "distancia_km": 3983,
        "temp": 22.5,
        "wind_spd": 6.0,
        "precip_1h": 0.0,
        "climate_severity_idx": 0.2,
        "dist_met_km": 12.0,
        "latitude": 40.64,
        "longitude": -73.78,
    }

    df_input = features_module.prepare_input_from_api(input_payload)
    df_input, feature_cols = feature_engineer.transform(df_input)

    proba = model.predict_proba(df_input[feature_cols])[:, 1][0]
    pred = int(model.predict(df_input[feature_cols])[0])

    output = {
        "input": input_payload,
        "probabilidad_retraso": round(float(proba), 6),
        "prediccion": pred,
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
