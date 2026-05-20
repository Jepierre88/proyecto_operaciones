from __future__ import annotations

from enum import Enum


class SolutionStatus(str, Enum):
    OPTIMAL = "OPTIMAL"
    MULTIPLE_OPTIMA = "MULTIPLE_OPTIMA"
    INFEASIBLE = "INFEASIBLE"
    UNBOUNDED = "UNBOUNDED"

    @property
    def is_solved(self) -> bool:
        return self in (SolutionStatus.OPTIMAL, SolutionStatus.MULTIPLE_OPTIMA)

    @property
    def description_es(self) -> str:
        return {
            SolutionStatus.OPTIMAL: "Optimo unico encontrado",
            SolutionStatus.MULTIPLE_OPTIMA: "Multiples soluciones optimas (optimo alterno)",
            SolutionStatus.INFEASIBLE: "Problema infactible (region factible vacia)",
            SolutionStatus.UNBOUNDED: "Problema no acotado",
        }[self]
