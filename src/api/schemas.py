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
    temp: float | None = Field(
        20.0,
        description="Temperatura (°C). Se asume 20.0 si no se envía.",
    )
    wind_spd: float | None = Field(
        5.0,
        description="Velocidad del viento (km/h). Se asume 5.0 si no se envía.",
    )
    precip_1h: float | None = Field(
        0.0,
        description="Precipitación última hora (mm). Se asume 0.0 si no se envía.",
    )
    climate_severity_idx: float | None = Field(
        0.0,
        description="Índice de severidad climática. Se asume 0.0 si no se envía.",
    )
    dist_met_km: float | None = Field(
        10.0,
        description="Distancia a estación meteorológica (km). Se asume 10.0 si no se envía.",
    )

    # Coordenadas
    latitude: float | None = Field(
        40.0,
        description="Latitud del aeropuerto. Se asume 40.0 si no se envía.",
    )
    longitude: float | None = Field(
        -74.0,
        description="Longitud del aeropuerto. Se asume -74.0 si no se envía.",
    )


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
