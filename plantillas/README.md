# Plantillas para cargar problemas

Estos archivos se cargan desde la app con **Archivo > Cargar problema...**

## Archivos disponibles

| Archivo | Que contiene |
|---|---|
| `plantilla_vacia.json` | Plantilla en blanco JSON: copiala y editala con tus datos |
| `plantilla_vacia.csv`  | Plantilla en blanco CSV: copiala y editala con tus datos |
| `ejemplo_fabrica.json` | Problema de la fabrica resuelto (Max Z = 3x + 5y, optimo (2,6) Z=36) |
| `ejemplo_dieta.csv`    | Problema de dieta minima (Min Z = 2x + 3y, optimo Z=13) |

## Formato JSON

```json
{
  "name": "Nombre del problema",
  "objective": {
    "type": "max",     // "max" o "min"
    "c1": 3,           // coeficiente de x en Z
    "c2": 5            // coeficiente de y en Z
  },
  "constraints": [
    {
      "a1": 1,         // coeficiente de x
      "a2": 0,         // coeficiente de y
      "op": "<=",      // "<=", ">=" o "="
      "b": 4,          // termino independiente
      "label": "..."   // opcional, etiqueta para el grafico
    }
  ]
}
```

**Notas**:
- No agregues `x >= 0` ni `y >= 0`: la app las incluye automaticamente (no-negatividad).
- El campo `label` es opcional pero se ve en la leyenda de la grafica.

## Formato CSV

Cada linea empieza con una etiqueta que indica que es esa fila:

```
name,<nombre del problema>
objective,<max|min>,<c1>,<c2>
constraint,<a1>,<a2>,<op>,<b>[,<label>]
constraint,<a1>,<a2>,<op>,<b>[,<label>]
...
```

**Notas**:
- El orden importa: primero `name`, luego `objective`, despues las `constraint`.
- El operador `op` debe ser `<=`, `>=` o `=`.
- El campo `label` es opcional (puede omitirse el ultimo valor).
- Separador estandar: coma (`,`). Si abris el CSV en Excel y lo guardas, asegurate de mantener comas y no punto-y-coma.

## Como crear tu propia plantilla rapidamente

1. Abri la app: `python main.py`
2. Llena los datos manualmente (o carga uno existente y modificalo).
3. Menu **Archivo > Guardar problema...** y elige nombre + ubicacion.
4. Listo: tenes un JSON valido que despues podes volver a cargar.
