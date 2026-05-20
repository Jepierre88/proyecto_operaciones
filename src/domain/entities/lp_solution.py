from __future__ import annotations

from dataclasses import dataclass, field

from src.domain.entities.constraint import Constraint
from src.domain.entities.vertex import Vertex
from src.domain.value_objects.solution_status import SolutionStatus


@dataclass(frozen=True)
class LPSolution:
    """Resultado de resolver un LPProblem por el metodo grafico."""

    status: SolutionStatus
    optimal_vertex: Vertex | None = None
    optimal_z: float | None = None
    all_vertices: tuple[Vertex, ...] = field(default_factory=tuple)
    alternative_optima: tuple[Vertex, ...] = field(default_factory=tuple)
    message: str = ""

    @property
    def is_solved(self) -> bool:
        return self.status.is_solved and self.optimal_vertex is not None
