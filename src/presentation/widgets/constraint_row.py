"""Una fila editable de restriccion: a1, a2, operador, b, boton eliminar."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from tkinter import ttk


class ConstraintRow(ttk.Frame):
    OPERATORS = ("<=", ">=", "=")

    def __init__(
        self,
        master: tk.Misc,
        on_delete: Callable[["ConstraintRow"], None],
        a1: float = 0,
        a2: float = 0,
        op: str = "<=",
        b: float = 0,
    ) -> None:
        super().__init__(master)
        self._on_delete = on_delete
        self._a1 = tk.StringVar(value=self._fmt(a1))
        self._a2 = tk.StringVar(value=self._fmt(a2))
        self._op = tk.StringVar(value=op)
        self._b = tk.StringVar(value=self._fmt(b))
        self._build()

    def _build(self) -> None:
        ttk.Entry(self, textvariable=self._a1, width=6, justify="right").pack(side="left")
        ttk.Label(self, text=" x  +  ").pack(side="left")
        ttk.Entry(self, textvariable=self._a2, width=6, justify="right").pack(side="left")
        ttk.Label(self, text=" y ").pack(side="left")
        op_combo = ttk.Combobox(
            self,
            textvariable=self._op,
            values=self.OPERATORS,
            state="readonly",
            width=4,
        )
        op_combo.pack(side="left", padx=4)
        ttk.Entry(self, textvariable=self._b, width=8, justify="right").pack(side="left")
        ttk.Button(self, text="X", width=2, command=self._delete_self).pack(
            side="left", padx=(8, 0)
        )

    def _delete_self(self) -> None:
        self._on_delete(self)

    def get_values(self) -> tuple[float, float, str, float]:
        return (
            self._parse(self._a1.get()),
            self._parse(self._a2.get()),
            self._op.get(),
            self._parse(self._b.get()),
        )

    @staticmethod
    def _parse(text: str) -> float:
        try:
            return float(text.replace(",", "."))
        except ValueError as exc:
            raise ValueError(f"Valor numerico invalido: {text!r}") from exc

    @staticmethod
    def _fmt(value: float) -> str:
        return f"{value:g}"
