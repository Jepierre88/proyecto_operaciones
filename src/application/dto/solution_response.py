"""DTO plano de salida para la UI / exportadores. Sin tipos del dominio."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class VertexRow:
    x: float
    y: float
    z: float
    is_optimal: bool = False
    active_constraints_text: str = ""


@dataclass
class SolutionResponse:
    status: str
    status_description: str
    problem_name: str
    objective_text: str
    constraints_text: list[str] = field(default_factory=list)
    optimal_x: float | None = None
    optimal_y: float | None = None
    optimal_z: float | None = None
    vertices: list[VertexRow] = field(default_factory=list)
    has_alternative_optima: bool = False
    message: str = ""
