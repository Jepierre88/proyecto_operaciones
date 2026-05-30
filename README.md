# Trabajo Final - Investigacion de Operaciones (Linea A)

Herramienta semiautomatizada para resolver problemas de **Programacion Lineal en 2 variables por el Metodo Grafico**.

Visualiza la region factible, enumera todos los vertices, evalua la funcion objetivo en cada uno y muestra el optimo.

## Estructura del proyecto (Clean Architecture)

```
src/
├── domain/              <- Logica pura del metodo grafico (sin UI ni I/O)
│   ├── entities/        <- Constraint, Objective, Vertex, LPProblem, LPSolution
│   ├── value_objects/   <- Operator, OptimizationType, SolutionStatus, Point
│   └── services/        <- VertexCalculator, FeasibilityChecker, OptimalSolver, UnboundednessDetector
├── application/         <- Casos de uso que orquestan el dominio
│   ├── dto/             <- ProblemRequest, SolutionResponse (DTOs planos)
│   ├── use_cases/       <- SolveLPProblem, LoadProblemFromFile, LoadSampleProblem, ExportResults
│   └── mappers/         <- ProblemMapper, SolutionMapper (DTO <-> dominio)
├── infrastructure/      <- Detalles externos (archivos, plotting)
│   ├── persistence/     <- JsonProblemLoader, CsvProblemLoader, CsvResultsExporter, PdfReportGenerator
│   ├── plotting/        <- MatplotlibFeasibleRegionPlotter
│   └── samples/         <- catalog.json + JsonSampleCatalog (problemas precargados)
└── presentation/        <- UI CustomTkinter (moderna, light/dark/system)
    ├── widgets/         <- ObjectiveForm, ConstraintRow, ConstraintsList, PlotCanvas, ResultsPanel, StatusBar
    ├── controllers/     <- MainController
    └── main_window.py
tests/                   <- Tests por capa (pytest)
main.py                  <- Composition Root (instancia y conecta todas las dependencias)
```

**Regla de dependencias**: `domain` no depende de nadie. `application` depende solo de `domain`. `infrastructure` y `presentation` dependen de `application` y `domain`. Las flechas apuntan hacia adentro.

## Como ejecutar

### 1. Crear entorno virtual

**Windows (PowerShell)**:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (cmd)** / Linux / Mac:
```bash
python -m venv .venv
.venv\Scripts\activate         # Windows
source .venv/bin/activate      # Linux/Mac
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicacion

```bash
python main.py
```

### 4. Correr los tests

```bash
pytest tests/ -v
```

## Como usar la herramienta

> La interfaz usa **CustomTkinter** (look moderno, esquinas redondeadas, dark mode). Cambia entre claro/oscuro/sistema con el dropdown "Tema" en la barra superior.

1. Al abrir la app se carga por defecto el **problema de la fabrica** (`Max Z = 3x + 5y`).
2. **Funcion objetivo**: elige Max/Min y escribe los coeficientes `c1` (de x) y `c2` (de y).
3. **Restricciones**: usa "+ Agregar restriccion" para sumar filas. Cada fila tiene `a1`, `a2`, operador (`<=`, `>=`, `=`) y termino independiente `b`. El boton **X** elimina una fila.
4. Pulsa **Resolver**.
5. Se muestra:
   - La region factible sombreada en verde.
   - Cada restriccion como una linea etiquetada.
   - Todos los vertices factibles marcados.
   - El optimo destacado con estrella roja y la curva de indiferencia `Z = Z*`.
   - Tabla con `(x, y, Z, restricciones activas)`, fila optima resaltada.
6. **Casos de prueba** (menu superior): 4 problemas clasicos precargados.
7. **Archivo > Cargar/Guardar problema**: lee/escribe `.json` (formato propio sencillo) o `.csv`.
8. **Exportar resultados**: genera en una carpeta `.png` del grafico, `.csv` con la tabla y `.pdf` listo para el informe tecnico.

## Caso de prueba canonico

Problema de la fabrica:

> Max Z = 3x + 5y
> s.a.  x ≤ 4
>       2y ≤ 12
>       3x + 2y ≤ 18
>       x, y ≥ 0

**Optimo conocido**: `(x, y) = (2, 6)`, `Z = 36`. La herramienta lo encuentra y esta cubierto por `tests/domain/test_optimal_solver.py`.

## Formato JSON de problemas

```json
{
  "name": "Mi problema",
  "objective": {"type": "max", "c1": 3, "c2": 5},
  "constraints": [
    {"a1": 1, "a2": 0, "op": "<=", "b": 4},
    {"a1": 3, "a2": 2, "op": "<=", "b": 18}
  ]
}
```

## Formato CSV de problemas

```
name,Mi problema
objective,max,3,5
constraint,1,0,<=,4
constraint,3,2,<=,18
```
