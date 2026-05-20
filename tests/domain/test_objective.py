from __future__ import annotations

from src.domain.entities.objective import Objective
from src.domain.value_objects.optimization_type import OptimizationType


def test_objective_evaluates_z_correctly():
    obj = Objective(c1=3, c2=5, optimization_type=OptimizationType.MAX)
    assert obj.evaluate(2, 6) == 36
    assert obj.evaluate(0, 0) == 0


def test_optimization_type_max_prefers_larger():
    t = OptimizationType.MAX
    assert t.is_better(10, 5)
    assert not t.is_better(5, 10)


def test_optimization_type_min_prefers_smaller():
    t = OptimizationType.MIN
    assert t.is_better(5, 10)
    assert not t.is_better(10, 5)
