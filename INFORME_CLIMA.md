# Informe Clima - Datos IATA

## Estado actual
- Ya existe el archivo de aeropuertos en `data/airports_be.csv`.
- Formato: columnas `iata,lat,lon`.
- Contenido: codigos IATA en mayusculas con latitud y longitud en decimal.

## Para tener en cuenta
- Este CSV permite resolver coordenadas sin usar geocoding externo.
- El backend puede usar este archivo para completar el clima por origen.
- Mantener el archivo actualizado si se agregan nuevos aeropuertos.
