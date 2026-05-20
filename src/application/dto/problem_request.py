"""DTO plano para recibir un problema desde la UI o un archivo. Sin tipos del dominio."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ConstraintRequest:
    a1: float
    a2: float
    operator: str  # "<=", ">=", "="
    b: float
    label: str = ""


@dataclass
class ProblemRequest:
    objective_type: str  # "max" | "min"
    c1: float
    c2: float
    constraints: list[ConstraintRequest] = field(default_factory=list)
    name: str = "Problema sin nombre"
