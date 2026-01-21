from __future__ import annotations

from dataclasses import dataclass

import joblib

from ..config import FEATURE_ENGINEER_PATH, METADATA_PATH, MODEL_PATH, PREDICTION_LABELS
from ..features import prepare_input_from_api
from ..modeling import FlightDelayModel
from .schemas import PredictionRequest, PredictionResponse


@dataclass
class PredictionService:
    model: FlightDelayModel
    feature_engineer: object

    @classmethod
    def load(cls) -> "PredictionService":
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"No se encontró el modelo en {MODEL_PATH}")
        if not METADATA_PATH.exists():
            raise FileNotFoundError(f"No se encontró metadata en {METADATA_PATH}")
        if not FEATURE_ENGINEER_PATH.exists():
            raise FileNotFoundError(f"No se encontró FeatureEngineer en {FEATURE_ENGINEER_PATH}")

        model = FlightDelayModel.load_model(str(MODEL_PATH), str(METADATA_PATH))
        feature_engineer = joblib.load(FEATURE_ENGINEER_PATH)
        return cls(model=model, feature_engineer=feature_engineer)

    def predict(self, request: PredictionRequest) -> PredictionResponse:
        input_payload = request.model_dump()
        raw_df = prepare_input_from_api(input_payload)
        transformed_df, _ = self.feature_engineer.transform(raw_df)

        required_features = self.model.feature_names or transformed_df.columns.tolist()
        missing_features = [col for col in required_features if col not in transformed_df.columns]
        if missing_features:
            raise ValueError(f"Faltan columnas requeridas: {', '.join(missing_features)}")

        X = transformed_df[required_features]
        probability = float(self.model.predict_proba(X)[0])
        prediction = int(probability >= self.model.best_threshold)
        label = PREDICTION_LABELS.get(prediction, str(prediction))

        return PredictionResponse(
            prediction=prediction,
            label=label,
            probability=probability,
            threshold=float(self.model.best_threshold),
            model_name=self.model.best_model_name,
        )
