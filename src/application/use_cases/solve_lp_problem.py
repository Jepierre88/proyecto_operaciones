"""Caso de uso principal: recibe ProblemRequest, resuelve, devuelve SolutionResponse + LPProblem."""

from __future__ import annotations

from dataclasses import dataclass

from src.application.dto.problem_request import ProblemRequest
from src.application.dto.solution_response import SolutionResponse
from src.application.mappers.problem_mapper import ProblemMapper
from src.application.mappers.solution_mapper import SolutionMapper
from src.domain.entities.lp_problem import LPProblem
from src.domain.entities.lp_solution import LPSolution
from src.domain.services.optimal_solver import OptimalSolver


@dataclass(frozen=True)
class SolveResult:
    """Empaqueta DTO + entidades de dominio (necesarias para el plotter)."""

    response: SolutionResponse
    problem: LPProblem
    solution: LPSolution


class SolveLPProblemUseCase:
    def __init__(self, solver: OptimalSolver) -> None:
        self._solver = solver

    def execute(self, request: ProblemRequest) -> SolveResult:
        problem = ProblemMapper.to_domain(request)
        solution = self._solver.solve(problem)
        response = SolutionMapper.to_response(solution, problem)
        return SolveResult(response=response, problem=problem, solution=solution)
