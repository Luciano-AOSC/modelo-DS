# JUSTIFICACION DEL THRESHOLD OPTIMIZADO
**Fecha**: 2026-01-13  
**Threshold final**: 0.5591  
**Decision**: Seleccionado por el optimizador de umbrales (precision/recall) con dataset completo

---

## RESUMEN EJECUTIVO

- **Umbral elegido**: 0.5591
- **Test set**: 5,350,283 registros (15% del dataset completo)
- **Criterio**: Maximizar F1 cumpliendo precision >= 0.35

---

## METRICAS EN TEST (THRESHOLD 0.5591)

| Metrica    | Valor  |
| ---------- | ------ |
| Accuracy   | 0.7232 |
| Precision  | 0.3501 |
| Recall     | 0.5430 |
| F1-Score   | 0.4257 |
| ROC-AUC    | 0.7194 |
| PR-AUC     | 0.3874 |

---

## MATRIZ DE CONFUSION (TEST)

```
                   Prediccion
                 Puntual  Retrasado
Real Puntual    3,319,108  1,018,723
     Retrasado    461,820    548,682
```

---

## JUSTIFICACION

- El umbral 0.5591 cumple la restriccion de precision (>= 0.35) y mantiene recall competitivo.
- El trade-off reduce falsas alertas sin perder demasiados retrasos detectados.
- Se mantiene un F1 estable con el dataset completo.

---

## NOTAS

- El analisis de umbrales se genera en `outputs/metrics/threshold_optimization.json`.
- Este umbral esta registrado en `models/metadata.json`.
