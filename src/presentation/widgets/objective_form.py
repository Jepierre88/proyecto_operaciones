"""Widget para capturar la funcion objetivo: tipo (max/min) y coeficientes c1, c2."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class ObjectiveForm(ttk.LabelFrame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, text="Funcion objetivo", padding=10)
        self._type_var = tk.StringVar(value="max")
        self._c1_var = tk.StringVar(value="3")
        self._c2_var = tk.StringVar(value="5")
        self._build()

    def _build(self) -> None:
        top = ttk.Frame(self)
        top.pack(anchor="w", pady=(0, 6))
        ttk.Radiobutton(top, text="Maximizar", variable=self._type_var, value="max").pack(
            side="left", padx=(0, 12)
        )
        ttk.Radiobutton(top, text="Minimizar", variable=self._type_var, value="min").pack(
            side="left"
        )

        row = ttk.Frame(self)
        row.pack(anchor="w")
        ttk.Label(row, text="Z =").pack(side="left", padx=(0, 4))
        ttk.Entry(row, textvariable=self._c1_var, width=8, justify="right").pack(side="left")
        ttk.Label(row, text=" x  +  ").pack(side="left")
        ttk.Entry(row, textvariable=self._c2_var, width=8, justify="right").pack(side="left")
        ttk.Label(row, text=" y").pack(side="left")

    def get_values(self) -> tuple[str, float, float]:
        return (
            self._type_var.get(),
            self._parse_float(self._c1_var.get()),
            self._parse_float(self._c2_var.get()),
        )

    def set_values(self, objective_type: str, c1: float, c2: float) -> None:
        self._type_var.set(objective_type)
        self._c1_var.set(self._format_number(c1))
        self._c2_var.set(self._format_number(c2))

    @staticmethod
    def _parse_float(text: str) -> float:
        try:
            return float(text.replace(",", "."))
        except ValueError as exc:
            raise ValueError(f"Coeficiente invalido: {text!r}") from exc

    @staticmethod
    def _format_number(value: float) -> str:
        return f"{value:g}"
