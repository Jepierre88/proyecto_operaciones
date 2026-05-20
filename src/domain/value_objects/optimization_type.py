from __future__ import annotations

from enum import Enum


class OptimizationType(str, Enum):
    MAX = "max"
    MIN = "min"

    @classmethod
    def from_string(cls, value: str) -> "OptimizationType":
        normalized = value.strip().lower()
        if normalized in ("max", "maximize", "maximizar"):
            return cls.MAX
        if normalized in ("min", "minimize", "minimizar"):
            return cls.MIN
        raise ValueError(f"Tipo de optimizacion no reconocido: {value!r}")

    def is_better(self, candidate: float, current_best: float, tolerance: float = 1e-9) -> bool:
        if self is OptimizationType.MAX:
            return candidate > current_best + tolerance
        return candidate < current_best - tolerance
