"""Contenedor dinamico de filas de restricciones con boton 'Agregar' y scroll."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from src.application.dto.problem_request import ConstraintRequest
from src.presentation.widgets.constraint_row import ConstraintRow


class ConstraintsList(ttk.LabelFrame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, text="Restricciones", padding=10)
        self._rows: list[ConstraintRow] = []
        self._build()

    def _build(self) -> None:
        # Scroll vertical para muchas restricciones
        outer = ttk.Frame(self)
        outer.pack(fill="both", expand=True)

        self._canvas = tk.Canvas(outer, highlightthickness=0, height=180)
        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=scrollbar.set)

        self._inner = ttk.Frame(self._canvas)
        self._inner.bind(
            "<Configure>",
            lambda _e: self._canvas.configure(scrollregion=self._canvas.bbox("all")),
        )
        self._canvas.create_window((0, 0), window=self._inner, anchor="nw")

        self._canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        ttk.Button(self, text="+ Agregar restriccion", command=self._add_empty).pack(
            anchor="w", pady=(8, 0)
        )

    def _add_empty(self) -> None:
        self.add_row()

    def add_row(self, a1: float = 0, a2: float = 0, op: str = "<=", b: float = 0) -> None:
        row = ConstraintRow(self._inner, on_delete=self._remove_row, a1=a1, a2=a2, op=op, b=b)
        row.pack(fill="x", pady=2)
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
