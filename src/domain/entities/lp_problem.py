from __future__ import annotations

from dataclasses import dataclass, field

from src.domain.entities.constraint import Constraint
from src.domain.entities.objective import Objective
from src.domain.value_objects.operator import Operator


@dataclass(frozen=True)
class LPProblem:
    """Problema completo de PL en 2 variables (x, y >= 0 implicito)."""

    objective: Objective
    constraints: tuple[Constraint, ...]
    name: str = "Problema sin nombre"
    include_non_negativity: bool = True

    def __post_init__(self) -> None:
        if not self.constraints:
            raise ValueError("El problema debe tener al menos una restriccion")

    @property
    def all_constraints(self) -> tuple[Constraint, ...]:
        """Restricciones del usuario + no-negatividad si aplica."""
        if not self.include_non_negativity:
            return self.constraints
        non_neg = (
            Constraint(a1=1.0, a2=0.0, operator=Operator.GE, b=0.0, label="x >= 0"),
            Constraint(a1=0.0, a2=1.0, operator=Operator.GE, b=0.0, label="y >= 0"),
        )
        return self.constraints + non_neg
