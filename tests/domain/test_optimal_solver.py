"""Tests del solver completo. Incluye el caso canonico de la fabrica (Max Z = 3x+5y)."""

from __future__ import annotations

import pytest

from src.domain.entities.constraint import Constraint
from src.domain.entities.lp_problem import LPProblem
from src.domain.entities.objective import Objective
from src.domain.services.feasibility_checker import FeasibilityChecker
from src.domain.services.optimal_solver import OptimalSolver
from src.domain.services.unboundedness_detector import UnboundednessDetector
from src.domain.services.vertex_calculator import VertexCalculator
from src.domain.value_objects.operator import Operator
from src.domain.value_objects.optimization_type import OptimizationType
from src.domain.value_objects.solution_status import SolutionStatus


@pytest.fixture
def solver() -> OptimalSolver:
    fc = FeasibilityChecker()
    return OptimalSolver(
        vertex_calculator=VertexCalculator(),
        feasibility_checker=fc,
        unboundedness_detector=UnboundednessDetector(fc),
    )


def _factory_problem() -> LPProblem:
    """Problema de la fabrica: Max Z = 3x + 5y s.a. x<=4, 2y<=12, 3x+2y<=18."""
    return LPProblem(
        objective=Objective(c1=3, c2=5, optimization_type=OptimizationType.MAX),
        constraints=(
            Constraint(a1=1, a2=0, operator=Operator.LE, b=4),
            Constraint(a1=0, a2=2, operator=Operator.LE, b=12),
            Constraint(a1=3, a2=2, operator=Operator.LE, b=18),
        ),
        name="Fabrica de muebles",
    )


def test_factory_problem_finds_known_optimum(solver):
    solution = solver.solve(_factory_problem())
    assert solution.status is SolutionStatus.OPTIMAL
    assert solution.optimal_vertex.x == pytest.approx(2.0, abs=1e-6)
    assert solution.optimal_vertex.y == pytest.approx(6.0, abs=1e-6)
    assert solution.optimal_z == pytest.approx(36.0, abs=1e-6)


def test_factory_problem_enumerates_all_feasible_vertices(solver):
    solution = solver.solve(_factory_problem())
    coords = {(round(v.x, 4), round(v.y, 4)) for v in solution.all_vertices}
    assert (0, 0) in coords
    assert (4, 0) in coords
    assert (4, 3) in coords
    assert (2, 6) in coords
    assert (0, 6) in coords


def test_infeasible_problem_reports_infeasibility(solver):
    problem = LPProblem(
        objective=Objective(c1=1, c2=1, optimization_type=OptimizationType.MAX),
        constraints=(
            Constraint(a1=1, a2=1, operator=Operator.LE, b=2),
            Constraint(a1=1, a2=1, operator=Operator.GE, b=5),
        ),
    )
    solution = solver.solve(problem)
    assert solution.status is SolutionStatus.INFEASIBLE
    assert solution.optimal_vertex is None


def test_unbounded_problem_is_detected(solver):
    problem = LPProblem(
        objective=Objective(c1=1, c2=1, optimization_type=OptimizationType.MAX),
        constraints=(Constraint(a1=1, a2=-1, operator=Operator.LE, b=1),),
    )
    solution = solver.solve(problem)
    assert solution.status is SolutionStatus.UNBOUNDED


def test_min_problem_finds_corner_minimum(solver):
    problem = LPProblem(
        objective=Objective(c1=2, c2=3, optimization_type=OptimizationType.MIN),
        constraints=(
            Constraint(a1=1, a2=1, operator=Operator.GE, b=4),
            Constraint(a1=1, a2=0, operator=Operator.LE, b=10),
            Constraint(a1=0, a2=1, operator=Operator.LE, b=10),
        ),
    )
    solution = solver.solve(problem)
    assert solution.status is SolutionStatus.OPTIMAL
    assert solution.optimal_z == pytest.approx(8.0, abs=1e-6)


def test_alternative_optima_are_detected(solver):
    problem = LPProblem(
        objective=Objective(c1=2, c2=4, optimization_type=OptimizationType.MAX),
        constraints=(
            Constraint(a1=1, a2=2, operator=Operator.LE, b=8),
            Constraint(a1=1, a2=0, operator=Operator.LE, b=6),
            Constraint(a1=0, a2=1, operator=Operator.LE, b=3),
        ),
    )
    solution = solver.solve(problem)
    assert solution.status is SolutionStatus.MULTIPLE_OPTIMA
    assert len(solution.alternative_optima) >= 1
