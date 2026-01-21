from fastapi import APIRouter, Depends, HTTPException, Request

from .schemas import PredictionRequest, PredictionResponse
from .service import PredictionService

router = APIRouter()


def get_service(request: Request) -> PredictionService:
    return request.app.state.prediction_service


@router.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@router.post("/predict", response_model=PredictionResponse)
def predict(
    request: PredictionRequest,
    service: PredictionService = Depends(get_service),
) -> PredictionResponse:
    try:
        return service.predict(request)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail={"error": "Faltan columnas requeridas", "details": str(exc)},
        ) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
