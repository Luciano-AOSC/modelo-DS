# modelo-DS

## API de predicción

Se agregó una API HTTP para consumir el modelo entrenado, organizada con esquemas (schemas), servicios y rutas, además de un patrón de factory de aplicación para alinearse con estructuras típicas como DS-modelo.

### Ejecutar la API

1. Instalar dependencias:

```bash
pip install -r requirements-runtime.md
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
  "aerolinea": "AA",
  "origen": "JFK",
  "destino": "LAX",
  "fecha_partida": "2025-03-15T14:30:00",
  "distancia_km": 3983,
  "temp": 21.5,
  "wind_spd": 4.2,
  "precip_1h": 0.0,
  "climate_severity_idx": 0.2,
  "dist_met_km": 8.0,
  "latitude": 40.64,
  "longitude": -73.78
}
```

Respuesta:

```json
{
  "prediction": 0,
  "label": "Puntual",
  "probability": 0.12,
  "threshold": 0.5591,
  "model_name": "XGBoost"
}
```
