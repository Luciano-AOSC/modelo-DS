# modelo-DS

## API de predicción

Se agregó una API HTTP para consumir el modelo entrenado, organizada con esquemas (schemas), servicios y rutas, además de un patrón de factory de aplicación para alinearse con estructuras típicas como DS-modelo.

### Ejecutar la API

1. Instalar dependencias:

```bash
pip install -r requirements.txt
```

2. Ejecutar el servidor (desde la raíz del repo):

```bash
uvicorn src.api:app --host 0.0.0.0 --port 8000
```

### Endpoint de predicción

`POST /predict`

Campos requeridos:

```json
{
  "flight": {
    "op_unique_carrier": "AA",
    "origin": "JFK",
    "dest": "LAX",
    "year": 2025,
    "month": 3,
    "day_of_week": 6,
    "day_of_month": 15,
    "dep_hour": 14,
    "sched_minute_of_day": 870,
    "distance": 2475,
    "temp": 21.5,
    "wind_spd": 15.3,
    "precip_1h": 0.0,
    "climate_severity_idx": 0.35,
    "dist_met_km": 12.5,
    "latitude": 40.6413,
    "longitude": -73.7781
  }
}
```

Respuesta:

```json
{
  "prediction": 0,
  "probability": 0.12,
  "threshold": 0.5591
}
```
