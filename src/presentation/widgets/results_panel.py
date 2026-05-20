"""Panel de resultados: estado + punto optimo + tabla de vertices."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from src.application.dto.solution_response import SolutionResponse


class ResultsPanel(ttk.LabelFrame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, text="Resultados", padding=10)
        self._status_var = tk.StringVar(value="(sin resolver)")
        self._optimum_var = tk.StringVar(value="")
        self._build()

    def _build(self) -> None:
        ttk.Label(self, textvariable=self._status_var, font=("TkDefaultFont", 10, "bold")).pack(
            anchor="w"
        )
        ttk.Label(self, textvariable=self._optimum_var, foreground="#1565c0").pack(
            anchor="w", pady=(2, 8)
        )

        columns = ("x", "y", "z", "active")
        self._tree = ttk.Treeview(self, columns=columns, show="headings", height=8)
        self._tree.heading("x", text="x")
        self._tree.heading("y", text="y")
        self._tree.heading("z", text="Z")
        self._tree.heading("active", text="Restricciones activas")
        self._tree.column("x", width=60, anchor="e")
        self._tree.column("y", width=60, anchor="e")
        self._tree.column("z", width=80, anchor="e")
        self._tree.column("active", width=240, anchor="w")
        self._tree.tag_configure("optimal", background="#fff3e0", font=("TkDefaultFont", 9, "bold"))
        self._tree.pack(fill="both", expand=True)

    def show(self, response: SolutionResponse) -> None:
        self._status_var.set(f"Estado: {response.status_description}")
        if response.optimal_x is not None:
            opt = f"Punto optimo: ({response.optimal_x:g}, {response.optimal_y:g})    Z = {response.optimal_z:g}"
            if response.has_alternative_optima:
                opt += "   (multiples soluciones optimas)"
            self._optimum_var.set(opt)
        else:
            self._optimum_var.set(response.message or "")
        self._tree.delete(*self._tree.get_children())
        for row in response.vertices:
            tags = ("optimal",) if row.is_optimal else ()
            marker = " *" if row.is_optimal else ""
            self._tree.insert(
                "",
                "end",
                values=(
                    f"{row.x:g}",
                    f"{row.y:g}",
                    f"{row.z:g}{marker}",
                    row.active_constraints_text,
                ),
                tags=tags,
            )

    def clear(self) -> None:
        self._status_var.set("(sin resolver)")
        self._optimum_var.set("")
        self._tree.delete(*self._tree.get_children())
