"""Carga ProblemRequest desde CSV.

Formato esperado (cabecera flexible, sin orden estricto):
Linea 1: name,<nombre del problema>
Linea 2: objective,<max|min>,<c1>,<c2>
Linea 3+: constraint,<a1>,<a2>,<op>,<b>[,<label>]
"""

from __future__ import annotations

import csv
from pathlib import Path

from src.application.dto.problem_request import ConstraintRequest, ProblemRequest


class CsvProblemLoader:
    def supports(self, path: Path) -> bool:
        return path.suffix.lower() == ".csv"

    def load(self, path: Path) -> ProblemRequest:
        name = "Problema sin nombre"
        objective_type = "max"
        c1, c2 = 0.0, 0.0
        constraints: list[ConstraintRequest] = []

        with path.open(encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row or not row[0].strip():
                    continue
                tag = row[0].strip().lower()
                if tag == "name" and len(row) >= 2:
                    name = row[1].strip()
                elif tag == "objective" and len(row) >= 4:
                    objective_type = row[1].strip().lower()
                    c1 = float(row[2])
                    c2 = float(row[3])
                elif tag == "constraint" and len(row) >= 5:
                    constraints.append(
                        ConstraintRequest(
                            a1=float(row[1]),
                            a2=float(row[2]),
                            operator=row[3].strip(),
                            b=float(row[4]),
                            label=row[5].strip() if len(row) >= 6 else "",
                        )
                    )

        return ProblemRequest(
            objective_type=objective_type,
            c1=c1,
            c2=c2,
            constraints=constraints,
            name=name,
        )
