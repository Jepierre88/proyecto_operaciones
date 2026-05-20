from __future__ import annotations

from enum import Enum


class Operator(str, Enum):
    LE = "<="
    GE = ">="
    EQ = "="

    @classmethod
    def from_symbol(cls, symbol: str) -> "Operator":
        symbol = symbol.strip()
        if symbol in ("<=", "≤", "=<"):
            return cls.LE
        if symbol in (">=", "≥", "=>"):
            return cls.GE
        if symbol in ("=", "=="):
            return cls.EQ
        raise ValueError(f"Operador no reconocido: {symbol!r}")

    def evaluate(self, lhs: float, rhs: float, tolerance: float = 1e-9) -> bool:
        if self is Operator.LE:
            return lhs <= rhs + tolerance
        if self is Operator.GE:
            return lhs >= rhs - tolerance
        return abs(lhs - rhs) <= tolerance
