"""Filtra puntos candidatos: solo los que satisfacen TODAS las restricciones son vertices factibles."""

from __future__ import annotations

from src.domain.entities.constraint import Constraint
from src.domain.entities.lp_problem import LPProblem
from src.domain.entities.vertex import Vertex
from src.domain.value_objects.point import Point


class FeasibilityChecker:
    def __init__(self, feasibility_tolerance: float = 1e-7, dedup_tolerance: float = 1e-7) -> None:
        self._tol = feasibility_tolerance
        self._dedup_tol = dedup_tolerance

    def filter_feasible(
        self,
        candidates: list[tuple[Point, tuple[Constraint, Constraint]]],
        problem: LPProblem,
    ) -> list[Vertex]:
        constraints = problem.all_constraints
        feasible: list[Vertex] = []

        for point, generators in candidates:
            if all(c.is_satisfied_by(point.x, point.y, self._tol) for c in constraints):
                active = tuple(c for c in constraints if c.is_active_at(point.x, point.y, self._tol))
                feasible.append(Vertex(point=point, active_constraints=active))

        return self._deduplicate(feasible)

    def _deduplicate(self, vertices: list[Vertex]) -> list[Vertex]:
        unique: list[Vertex] = []
        for v in vertices:
            if not any(v.point.is_close_to(u.point, self._dedup_tol) for u in unique):
                unique.append(v)
        return unique

    def is_point_feasible(self, point: Point, problem: LPProblem) -> bool:
        return all(c.is_satisfied_by(point.x, point.y, self._tol) for c in problem.all_constraints)
