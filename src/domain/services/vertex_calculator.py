"""Genera puntos candidatos a vertice resolviendo el sistema 2x2 de cada par de restricciones."""

from __future__ import annotations

from itertools import combinations

import numpy as np

from src.domain.entities.constraint import Constraint
from src.domain.entities.lp_problem import LPProblem
from src.domain.value_objects.point import Point

PARALLEL_DET_TOLERANCE = 1e-12


class VertexCalculator:
    def __init__(self, parallel_tolerance: float = PARALLEL_DET_TOLERANCE) -> None:
        self._tolerance = parallel_tolerance

    def compute_candidate_vertices(
        self, problem: LPProblem
    ) -> list[tuple[Point, tuple[Constraint, Constraint]]]:
        """Devuelve todos los puntos de interseccion de pares de restricciones.

        Cada elemento es (Point, (Constraint_i, Constraint_j)). Las restricciones
        de no-negatividad se incluyen automaticamente para generar los cortes con ejes.
        """
        constraints = problem.all_constraints
        candidates: list[tuple[Point, tuple[Constraint, Constraint]]] = []

        for c1, c2 in combinations(constraints, 2):
            point = self._intersect(c1, c2)
            if point is not None:
                candidates.append((point, (c1, c2)))

        return candidates

    def _intersect(self, c1: Constraint, c2: Constraint) -> Point | None:
        """Resuelve [a1 a2; a1' a2'] [x; y] = [b; b']. None si rectas paralelas."""
        matrix = np.array([[c1.a1, c1.a2], [c2.a1, c2.a2]], dtype=float)
        rhs = np.array([c1.b, c2.b], dtype=float)
        det = np.linalg.det(matrix)
        if abs(det) < self._tolerance:
            return None
        solution = np.linalg.solve(matrix, rhs)
        return Point(x=float(solution[0]), y=float(solution[1]))
