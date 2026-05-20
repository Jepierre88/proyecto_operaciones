from __future__ import annotations

import pytest

from src.application.services.solution_explainer import SolutionExplainer
from src.domain.entities.constraint import Constraint
from src.domain.entities.lp_problem import LPProblem
from src.domain.entities.objective import Objective
from src.domain.services.feasibility_checker import FeasibilityChecker
from src.domain.services.optimal_solver import OptimalSolver
from src.domain.services.unboundedness_detector import UnboundednessDetector
from src.domain.services.vertex_calculator import VertexCalculator
from src.domain.value_objects.operator import Operator
from src.domain.value_objects.optimization_type import OptimizationType


@pytest.fixture
def solver() -> OptimalSolver:
    fc = FeasibilityChecker()
    return OptimalSolver(VertexCalculator(), fc, UnboundednessDetector(fc))


@pytest.fixture
def explainer() -> SolutionExplainer:
    return SolutionExplainer()


def _factory_problem() -> LPProblem:
    return LPProblem(
        objective=Objective(c1=3, c2=5, optimization_type=OptimizationType.MAX),
        constraints=(
            Constraint(a1=1, a2=0, operator=Operator.LE, b=4),
            Constraint(a1=0, a2=2, operator=Operator.LE, b=12),
            Constraint(a1=3, a2=2, operator=Operator.LE, b=18),
        ),
        name="Fabrica",
    )


def test_explainer_generates_seven_steps_for_solved_problem(solver, explainer):
    problem = _factory_problem()
    solution = solver.solve(problem)
    steps = explainer.explain(problem, solution)
    assert len(steps) == 7
    titles = [s.title for s in steps]
    assert any("Planteamiento" in t for t in titles)
    assert any("Estrategia" in t for t in titles)
    assert any("Intersecciones" in t for t in titles)
    assert any("Filtrado" in t for t in titles)
    assert any("Evaluacion" in t for t in titles)
    assert any("Seleccion" in t for t in titles)
    assert any("activas" in t.lower() for t in titles)


def test_explainer_includes_concrete_values_from_problem(solver, explainer):
    problem = _factory_problem()
    solution = solver.solve(problem)
    steps = explainer.explain(problem, solution)
    full_text = "\n".join(s.content for s in steps)
    # El optimo del problema fabrica es (2,6) con Z=36
    assert "36" in full_text
    assert "(2, 6)" in full_text or "2, 6" in full_text


def test_explainer_handles_infeasible_problem(solver, explainer):
    problem = LPProblem(
        objective=Objective(c1=1, c2=1, optimization_type=OptimizationType.MAX),
        constraints=(
            Constraint(a1=1, a2=1, operator=Operator.LE, b=2),
            Constraint(a1=1, a2=1, operator=Operator.GE, b=5),
        ),
    )
    solution = solver.solve(problem)
    steps = explainer.explain(problem, solution)
    full_text = "\n".join(s.content for s in steps)
    assert "INFACTIBLE" in full_text.upper() or "VACIA" in full_text.upper()
    assert len(steps) < 7


def test_explainer_handles_unbounded_problem(solver, explainer):
    problem = LPProblem(
        objective=Objective(c1=1, c2=1, optimization_type=OptimizationType.MAX),
        constraints=(Constraint(a1=1, a2=-1, operator=Operator.LE, b=1),),
    )
    solution = solver.solve(problem)
    steps = explainer.explain(problem, solution)
    full_text = "\n".join(s.content for s in steps)
    assert "ACOTADO" in full_text.upper()


def test_explainer_steps_have_nonempty_content(solver, explainer):
    problem = _factory_problem()
    solution = solver.solve(problem)
    steps = explainer.explain(problem, solution)
    for step in steps:
        assert step.title.strip()
        assert step.content.strip()
        assert len(step.content.splitlines()) >= 3
