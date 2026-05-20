"""Orquesta el metodo grafico: candidatos -> factibles -> evaluar Z -> elegir optimo."""

from __future__ import annotations

from dataclasses import replace

from src.domain.entities.lp_problem import LPProblem
from src.domain.entities.lp_solution import LPSolution
from src.domain.entities.vertex import Vertex
from src.domain.services.feasibility_checker import FeasibilityChecker
from src.domain.services.unboundedness_detector import UnboundednessDetector
from src.domain.services.vertex_calculator import VertexCalculator
from src.domain.value_objects.solution_status import SolutionStatus

ALTERNATE_OPTIMA_TOLERANCE = 1e-7


class OptimalSolver:
    def __init__(
        self,
        vertex_calculator: VertexCalculator,
        feasibility_checker: FeasibilityChecker,
        unboundedness_detector: UnboundednessDetector,
    ) -> None:
        self._vertices = vertex_calculator
        self._feasibility = feasibility_checker
        self._unbounded = unboundedness_detector

    def solve(self, problem: LPProblem) -> LPSolution:
        candidates = self._vertices.compute_candidate_vertices(problem)
        feasible = self._feasibility.filter_feasible(candidates, problem)

        if not feasible:
            return LPSolution(
                status=SolutionStatus.INFEASIBLE,
                message="No existe punto que satisfaga simultaneamente todas las restricciones.",
            )

        evaluated = tuple(
            replace(v, z_value=problem.objective.evaluate(v.x, v.y)) for v in feasible
        )

        if self._unbounded.is_unbounded(problem, list(evaluated)):
            return LPSolution(
                status=SolutionStatus.UNBOUNDED,
                all_vertices=evaluated,
                message="La funcion objetivo puede mejorarse indefinidamente dentro de la region factible.",
            )

        optimal = self._pick_optimal(evaluated, problem)
        alternates = self._find_alternates(evaluated, optimal)

        status = SolutionStatus.MULTIPLE_OPTIMA if alternates else SolutionStatus.OPTIMAL
        return LPSolution(
            status=status,
            optimal_vertex=optimal,
            optimal_z=optimal.z_value,
            all_vertices=evaluated,
            alternative_optima=tuple(alternates),
            message=status.description_es,
        )

    def _pick_optimal(self, vertices: tuple[Vertex, ...], problem: LPProblem) -> Vertex:
        best = vertices[0]
        for v in vertices[1:]:
            if problem.objective.optimization_type.is_better(v.z_value, best.z_value):
                best = v
        return best

    def _find_alternates(self, vertices: tuple[Vertex, ...], optimal: Vertex) -> list[Vertex]:
        return [
            v
            for v in vertices
            if v is not optimal
            and abs(v.z_value - optimal.z_value) <= ALTERNATE_OPTIMA_TOLERANCE
        ]
