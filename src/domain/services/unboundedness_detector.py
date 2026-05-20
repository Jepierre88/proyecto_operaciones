"""Detecta si un problema es no acotado evaluando si Z mejora al alejarse en direcciones factibles.

Estrategia: si existe un vertice factible, se evalua si moviendose desde el por
las direcciones de las aristas de la region factible Z puede crecer (o decrecer)
indefinidamente. Implementacion simplificada: si no hay vertice optimo finito
pero la region factible no es vacia, se considera no acotado.

Heuristica practica: tomar el centroide de los vertices y un punto muy alejado en
la direccion del gradiente; si ese punto es factible, el problema es no acotado.
"""

from __future__ import annotations

from src.domain.entities.lp_problem import LPProblem
from src.domain.entities.vertex import Vertex
from src.domain.services.feasibility_checker import FeasibilityChecker
from src.domain.value_objects.optimization_type import OptimizationType
from src.domain.value_objects.point import Point


class UnboundednessDetector:
    LARGE_STEP = 1e9

    def __init__(self, feasibility_checker: FeasibilityChecker) -> None:
        self._feasibility = feasibility_checker

    def is_unbounded(self, problem: LPProblem, feasible_vertices: list[Vertex]) -> bool:
        if not feasible_vertices:
            return False

        direction_x, direction_y = self._improving_direction(problem)
        if direction_x == 0 and direction_y == 0:
            return False

        start = feasible_vertices[0].point
        far_point = Point(
            x=start.x + direction_x * self.LARGE_STEP,
            y=start.y + direction_y * self.LARGE_STEP,
        )
        return self._feasibility.is_point_feasible(far_point, problem)

    def _improving_direction(self, problem: LPProblem) -> tuple[float, float]:
        c1, c2 = problem.objective.c1, problem.objective.c2
        if problem.objective.optimization_type is OptimizationType.MAX:
            return (c1, c2)
        return (-c1, -c2)
