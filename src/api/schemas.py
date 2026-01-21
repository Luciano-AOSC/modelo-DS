from typing import Optional

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    aerolinea: str = Field(..., min_length=1, description="Código de aerolínea (IATA/ICAO)")
    origen: str = Field(..., min_length=1, description="Aeropuerto origen (IATA)")
    destino: str = Field(..., min_length=1, description="Aeropuerto destino (IATA)")
    fecha_partida: str = Field(..., description="Fecha/hora en ISO-8601, ej: 2025-03-15T14:30:00")
    distancia_km: float = Field(..., gt=0, description="Distancia del vuelo en kilómetros")

    temp: Optional[float] = Field(20.0, description="Temperatura en °C")
    wind_spd: Optional[float] = Field(5.0, description="Velocidad del viento")
    precip_1h: Optional[float] = Field(0.0, description="Precipitación última hora")
    climate_severity_idx: Optional[float] = Field(0.0, description="Índice de severidad climática")
    dist_met_km: Optional[float] = Field(10.0, description="Distancia a estación meteorológica (km)")
    latitude: Optional[float] = Field(40.0, description="Latitud del aeropuerto")
    longitude: Optional[float] = Field(-74.0, description="Longitud del aeropuerto")


class PredictionResponse(BaseModel):
    prediction: int
    label: str
    probability: float
    threshold: float
    model_name: str
