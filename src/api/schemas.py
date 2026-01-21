from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    aerolinea: str = Field(..., min_length=1, description="Código de aerolínea (IATA/ICAO)")
    origen: str = Field(..., min_length=1, description="Aeropuerto origen (IATA)")
    destino: str = Field(..., min_length=1, description="Aeropuerto destino (IATA)")
    fecha_partida: str = Field(..., description="Fecha/hora en ISO-8601, ej: 2025-03-15T14:30:00")
    distancia_km: float = Field(..., gt=0, description="Distancia del vuelo en kilómetros")

    temp: float = Field(..., description="Temperatura en °C")
    wind_spd: float = Field(..., description="Velocidad del viento")
    precip_1h: float = Field(..., description="Precipitación última hora")
    climate_severity_idx: float = Field(..., description="Índice de severidad climática")
    dist_met_km: float = Field(..., description="Distancia a estación meteorológica (km)")
    latitude: float = Field(..., description="Latitud del aeropuerto")
    longitude: float = Field(..., description="Longitud del aeropuerto")


class PredictionResponse(BaseModel):
    prediction: int
    label: str
    probability: float
    threshold: float
    model_name: str
