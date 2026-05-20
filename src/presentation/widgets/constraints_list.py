"""Contenedor dinamico de filas de restricciones con scroll (CustomTkinter)."""

from __future__ import annotations

import customtkinter as ctk

from src.application.dto.problem_request import ConstraintRequest
from src.presentation.widgets.constraint_row import ConstraintRow


class ConstraintsList(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, corner_radius=10)
        self._rows: list[ConstraintRow] = []
        self._build()

    def _build(self) -> None:
        ctk.CTkLabel(
            self, text="Restricciones", font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=14, pady=(12, 8))

        self._scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", height=180)
        self._scroll.pack(fill="both", expand=True, padx=10, pady=(0, 8))

        ctk.CTkButton(
            self,
            text="+ Agregar restriccion",
            command=self._add_empty,
            anchor="w",
        ).pack(fill="x", padx=14, pady=(0, 12))

    def _add_empty(self) -> None:
        self.add_row()

    def add_row(self, a1: float = 0, a2: float = 0, op: str = "<=", b: float = 0) -> None:
        row = ConstraintRow(self._scroll, on_delete=self._remove_row, a1=a1, a2=a2, op=op, b=b)
        row.pack(fill="x", pady=4, padx=2)
        self._rows.append(row)

    def _remove_row(self, row: ConstraintRow) -> None:
        if row in self._rows:
            self._rows.remove(row)
            row.destroy()

    def clear(self) -> None:
        for row in list(self._rows):
            row.destroy()
        self._rows.clear()

    def set_from_requests(self, requests: list[ConstraintRequest]) -> None:
        self.clear()
        for c in requests:
            self.add_row(a1=c.a1, a2=c.a2, op=c.operator, b=c.b)

    def get_values(self) -> list[tuple[float, float, str, float]]:
        return [row.get_values() for row in self._rows]
