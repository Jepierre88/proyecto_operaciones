from __future__ import annotations

from src.domain.entities.constraint import Constraint
from src.domain.entities.lp_problem import LPProblem
from src.domain.entities.objective import Objective
from src.domain.services.vertex_calculator import VertexCalculator
from src.domain.value_objects.operator import Operator
from src.domain.value_objects.optimization_type import OptimizationType


def _problem(constraints: list[Constraint]) -> LPProblem:
    objective = Objective(c1=1, c2=1, optimization_type=OptimizationType.MAX)
    return LPProblem(objective=objective, constraints=tuple(constraints))


def test_vertex_calculator_intersects_orthogonal_lines():
    calc = VertexCalculator()
    constraints = [
        Constraint(a1=1, a2=0, operator=Operator.LE, b=4),
        Constraint(a1=0, a2=1, operator=Operator.LE, b=3),
    ]
    points = calc.compute_candidate_vertices(_problem(constraints))
    coords = {(round(p.x, 6), round(p.y, 6)) for p, _ in points}
    assert (4.0, 3.0) in coords
    assert (0.0, 0.0) in coords
    assert (4.0, 0.0) in coords
    assert (0.0, 3.0) in coords


def test_vertex_calculator_skips_parallel_lines():
    calc = VertexCalculator()
    constraints = [
        Constraint(a1=1, a2=1, operator=Operator.LE, b=4),
        Constraint(a1=2, a2=2, operator=Operator.LE, b=10),
    ]
    points = calc.compute_candidate_vertices(_problem(constraints))
    coords = [(p.x, p.y) for p, _ in points]
    for x, y in coords:
        assert not (abs(x - y - 0) < 1e9 and abs(x + y) > 1e8)
