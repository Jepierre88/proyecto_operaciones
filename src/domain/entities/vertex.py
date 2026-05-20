from __future__ import annotations

from dataclasses import dataclass, field

from src.domain.entities.constraint import Constraint
from src.domain.value_objects.point import Point


@dataclass(frozen=True)
class Vertex:
    """Punto factible que es interseccion de dos o mas restricciones activas."""

    point: Point
    active_constraints: tuple[Constraint, ...] = field(default_factory=tuple)
    z_value: float = 0.0

    @property
    def x(self) -> float:
        return self.point.x

    @property
    def y(self) -> float:
        return self.point.y
