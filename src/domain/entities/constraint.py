from __future__ import annotations

from dataclasses import dataclass

from src.domain.value_objects.operator import Operator


@dataclass(frozen=True)
class Constraint:
    """Restriccion lineal: a1*x + a2*y {op} b."""

    a1: float
    a2: float
    operator: Operator
    b: float
    label: str = ""

    def __post_init__(self) -> None:
        if self.a1 == 0 and self.a2 == 0:
            raise ValueError("La restriccion no puede tener ambos coeficientes en cero")

    def lhs_value(self, x: float, y: float) -> float:
        return self.a1 * x + self.a2 * y

    def is_satisfied_by(self, x: float, y: float, tolerance: float = 1e-9) -> bool:
        return self.operator.evaluate(self.lhs_value(x, y), self.b, tolerance)

    def is_active_at(self, x: float, y: float, tolerance: float = 1e-7) -> bool:
        return abs(self.lhs_value(x, y) - self.b) <= tolerance

    def as_pretty_string(self) -> str:
        def _coef(coef: float, var: str) -> str:
            if coef == 0:
                return ""
            if coef == 1:
                return f"+ {var}"
            if coef == -1:
                return f"- {var}"
            sign = "+" if coef > 0 else "-"
            return f"{sign} {abs(coef):g}{var}"

        parts = []
        first_x = self.a1 != 0
        if self.a1 != 0:
            if self.a1 < 0:
                parts.append(f"-{abs(self.a1):g}x" if abs(self.a1) != 1 else "-x")
            else:
                parts.append(f"{self.a1:g}x" if self.a1 != 1 else "x")
        if self.a2 != 0:
            piece = _coef(self.a2, "y")
            if not first_x and self.a2 > 0:
                piece = piece.replace("+ ", "")
            parts.append(piece)
        lhs = " ".join(parts) if parts else "0"
        return f"{lhs} {self.operator.value} {self.b:g}"
