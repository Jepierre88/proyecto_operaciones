from __future__ import annotations

from dataclasses import dataclass
from math import isclose


@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def is_close_to(self, other: "Point", tolerance: float = 1e-7) -> bool:
        return isclose(self.x, other.x, abs_tol=tolerance) and isclose(
            self.y, other.y, abs_tol=tolerance
        )

    def as_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)
