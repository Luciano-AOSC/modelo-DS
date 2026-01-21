"""
FlightOnTime - API de Predicción
================================
Servicio HTTP para exponer el modelo de retrasos.
"""

from fastapi import FastAPI

from .routes import router
from .service import PredictionService


def create_app() -> FastAPI:
    app = FastAPI(
        title="FlightOnTime Prediction API",
        version="1.0.0",
        description="API para predecir retrasos de vuelos usando el modelo entrenado.",
    )

    @app.on_event("startup")
    def startup_event() -> None:
        app.state.prediction_service = PredictionService.load()

    app.include_router(router)
    return app


app = create_app()
