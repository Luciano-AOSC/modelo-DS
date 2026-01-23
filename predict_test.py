import json

import joblib

from src.config import FEATURE_ENGINEER_PATH, MODEL_PATH
from src.features import prepare_input_from_api


def main() -> None:
    with open(MODEL_PATH, "rb") as model_file:
        model = joblib.load(model_file)
    with open(FEATURE_ENGINEER_PATH, "rb") as fe_file:
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

    df_input = prepare_input_from_api(input_payload)
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
