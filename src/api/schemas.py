"""
Schemas/DTOs de entrada y salida para la API.
"""

from pydantic import BaseModel, Field


class FlightPayload(BaseModel):
    """
    DTO con los datos del vuelo para la predicción.
    """

    # Identificadores
    op_unique_carrier: str = Field(..., description="Código de la aerolínea (ej: AA).")
    origin: str = Field(..., description="Aeropuerto de origen (IATA).")
    dest: str = Field(..., description="Aeropuerto de destino (IATA).")

    # Variables temporales
    year: int = Field(..., description="Año del vuelo.")
    month: int = Field(..., description="Mes del vuelo (1-12).")
    day_of_week: int = Field(..., description="Día de la semana (1=Lun, 7=Dom).")
    day_of_month: int = Field(..., description="Día del mes (1-31).")
    dep_hour: int = Field(..., description="Hora programada de salida (0-23).")
    sched_minute_of_day: int = Field(..., description="Minuto del día (0-1439).")

    # Distancia y clima
    distance: float = Field(..., description="Distancia del vuelo en millas.")
    temp: float = Field(..., description="Temperatura (°C).")
    wind_spd: float = Field(..., description="Velocidad del viento (km/h).")
    precip_1h: float = Field(..., description="Precipitación última hora (mm).")
    climate_severity_idx: float = Field(..., description="Índice de severidad climática.")
    dist_met_km: float = Field(..., description="Distancia a estación meteorológica (km).")

    # Coordenadas
    latitude: float = Field(..., description="Latitud del aeropuerto.")
    longitude: float = Field(..., description="Longitud del aeropuerto.")


class PredictionRequest(BaseModel):
    """
    DTO de entrada.
    """

    flight: FlightPayload = Field(..., description="Vuelo a predecir.")


class PredictionResponse(BaseModel):
    """
    DTO de salida.
    """

    prediction: int
    probability: float
    threshold: float
