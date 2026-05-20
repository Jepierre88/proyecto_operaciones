"""Exporta la tabla de vertices y resumen del problema a CSV."""

from __future__ import annotations

import csv
from pathlib import Path

from src.application.dto.solution_response import SolutionResponse


class CsvResultsExporter:
    def export_csv(self, response: SolutionResponse, path: Path) -> None:
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Problema", response.problem_name])
            writer.writerow(["Funcion Objetivo", response.objective_text])
            writer.writerow(["Estado", response.status_description])
            if response.optimal_x is not None:
                writer.writerow(
                    [
                        "Optimo",
                        f"x={response.optimal_x:g}",
                        f"y={response.optimal_y:g}",
                        f"Z={response.optimal_z:g}",
                    ]
                )
            writer.writerow([])
            writer.writerow(["Restricciones"])
            for text in response.constraints_text:
                writer.writerow([text])
            writer.writerow([])
            writer.writerow(["x", "y", "Z", "Optimo", "Restricciones activas"])
            for row in response.vertices:
                writer.writerow(
                    [
                        f"{row.x:g}",
                        f"{row.y:g}",
                        f"{row.z:g}",
                        "SI" if row.is_optimal else "",
                        row.active_constraints_text,
                    ]
                )
