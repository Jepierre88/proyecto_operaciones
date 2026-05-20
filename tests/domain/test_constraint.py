from __future__ import annotations

import pytest

from src.domain.entities.constraint import Constraint
from src.domain.value_objects.operator import Operator


def test_constraint_le_is_satisfied():
    c = Constraint(a1=1, a2=0, operator=Operator.LE, b=4)
    assert c.is_satisfied_by(3, 0)
    assert c.is_satisfied_by(4, 0)
    assert not c.is_satisfied_by(5, 0)


def test_constraint_ge_is_satisfied():
    c = Constraint(a1=0, a2=1, operator=Operator.GE, b=2)
    assert not c.is_satisfied_by(0, 1)
    assert c.is_satisfied_by(0, 2)
    assert c.is_satisfied_by(0, 5)


def test_constraint_eq_is_satisfied_with_tolerance():
    c = Constraint(a1=1, a2=1, operator=Operator.EQ, b=10)
    assert c.is_satisfied_by(5, 5)
    assert c.is_satisfied_by(5.0000000001, 5)
    assert not c.is_satisfied_by(5, 6)


def test_constraint_active_at_detects_on_boundary():
    c = Constraint(a1=3, a2=2, operator=Operator.LE, b=18)
    assert c.is_active_at(2, 6)
    assert not c.is_active_at(0, 0)


def test_constraint_rejects_zero_coefficients():
    with pytest.raises(ValueError):
        Constraint(a1=0, a2=0, operator=Operator.LE, b=5)
