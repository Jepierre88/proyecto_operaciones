from __future__ import annotations

from dataclasses import dataclass

from src.domain.value_objects.optimization_type import OptimizationType


@dataclass(frozen=True)
class Objective:
    """Funcion objetivo: Z = c1*x + c2*y, a maximizar o minimizar."""

    c1: float
    c2: float
    optimization_type: OptimizationType

    def evaluate(self, x: float, y: float) -> float:
        return self.c1 * x + self.c2 * y

    def as_pretty_string(self) -> str:
        verb = "Max" if self.optimization_type is OptimizationType.MAX else "Min"
        parts = []
        if self.c1 != 0:
            if self.c1 == 1:
                parts.append("x")
            elif self.c1 == -1:
                parts.append("-x")
            else:
                parts.append(f"{self.c1:g}x")
        if self.c2 != 0:
            sign = "+" if self.c2 > 0 and parts else ("-" if self.c2 < 0 else "+")
            coef = abs(self.c2)
            term = "y" if coef == 1 else f"{coef:g}y"
            if parts:
                parts.append(f"{sign} {term}")
            else:
                parts.append(term if self.c2 > 0 else f"-{term}")
        expr = " ".join(parts) if parts else "0"
        return f"{verb} Z = {expr}"
