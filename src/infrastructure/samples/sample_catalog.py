"""Lee el catalogo de problemas precargados desde catalog.json."""

from __future__ import annotations

import json
from pathlib import Path

from src.application.dto.problem_request import ConstraintRequest, ProblemRequest


class JsonSampleCatalog:
    def __init__(self, catalog_path: Path | None = None) -> None:
        self._catalog_path = catalog_path or Path(__file__).parent / "catalog.json"
        self._cache: dict | None = None

    def _load_catalog(self) -> dict:
        if self._cache is None:
            self._cache = json.loads(self._catalog_path.read_text(encoding="utf-8"))
        return self._cache

    def list_samples(self) -> list[tuple[str, str]]:
        catalog = self._load_catalog()
        return [(s["id"], s["display_name"]) for s in catalog["samples"]]

    def get_sample(self, sample_id: str) -> ProblemRequest:
        catalog = self._load_catalog()
        for sample in catalog["samples"]:
            if sample["id"] == sample_id:
                return self._to_request(sample["problem"])
        raise KeyError(f"Sample no encontrado: {sample_id!r}")

    @staticmethod
    def _to_request(data: dict) -> ProblemRequest:
        objective = data.get("objective", {})
        return ProblemRequest(
            objective_type=objective.get("type", "max"),
            c1=float(objective.get("c1", 0)),
            c2=float(objective.get("c2", 0)),
            constraints=[
                ConstraintRequest(
                    a1=float(c["a1"]),
                    a2=float(c["a2"]),
                    operator=str(c["op"]),
                    b=float(c["b"]),
                    label=str(c.get("label", "")),
                )
                for c in data.get("constraints", [])
            ],
            name=str(data.get("name", "Problema sin nombre")),
        )
