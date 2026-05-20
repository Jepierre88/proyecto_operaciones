"""Carga/guarda ProblemRequest en formato JSON.

Esquema:
{
  "name": "...",
  "objective": {"type": "max" | "min", "c1": <num>, "c2": <num>},
  "constraints": [
    {"a1": <num>, "a2": <num>, "op": "<=" | ">=" | "=", "b": <num>, "label": "..."},
    ...
  ]
}
"""

from __future__ import annotations

import json
from pathlib import Path

from src.application.dto.problem_request import ConstraintRequest, ProblemRequest


class JsonProblemLoader:
    def supports(self, path: Path) -> bool:
        return path.suffix.lower() == ".json"

    def load(self, path: Path) -> ProblemRequest:
        data = json.loads(path.read_text(encoding="utf-8"))
        objective = data.get("objective", {})
        constraints_raw = data.get("constraints", [])
        return ProblemRequest(
            objective_type=objective.get("type", "max"),
            c1=float(objective.get("c1", 0)),
            c2=float(objective.get("c2", 0)),
            constraints=[
                ConstraintRequest(
                    a1=float(c.get("a1", 0)),
                    a2=float(c.get("a2", 0)),
                    operator=str(c.get("op", "<=")),
                    b=float(c.get("b", 0)),
                    label=str(c.get("label", "")),
                )
                for c in constraints_raw
            ],
            name=str(data.get("name", "Problema sin nombre")),
        )

    def save(self, request: ProblemRequest, path: Path) -> None:
        payload = {
            "name": request.name,
            "objective": {
                "type": request.objective_type,
                "c1": request.c1,
                "c2": request.c2,
            },
            "constraints": [
                {"a1": c.a1, "a2": c.a2, "op": c.operator, "b": c.b, "label": c.label}
                for c in request.constraints
            ],
        }
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
