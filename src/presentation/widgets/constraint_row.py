"""Una fila editable de restriccion (CustomTkinter)."""

from __future__ import annotations

from collections.abc import Callable

import customtkinter as ctk


class ConstraintRow(ctk.CTkFrame):
    OPERATORS = ("<=", ">=", "=")

    def __init__(
        self,
        master,
        on_delete: Callable[["ConstraintRow"], None],
        a1: float = 0,
        a2: float = 0,
        op: str = "<=",
        b: float = 0,
    ) -> None:
        super().__init__(master, fg_color="transparent")
        self._on_delete = on_delete
        self._a1 = ctk.StringVar(value=self._fmt(a1))
        self._a2 = ctk.StringVar(value=self._fmt(a2))
        self._op = ctk.StringVar(value=op)
        self._b = ctk.StringVar(value=self._fmt(b))
        self._build()

    def _build(self) -> None:
        ctk.CTkEntry(self, textvariable=self._a1, width=60, justify="right").pack(side="left")
        ctk.CTkLabel(self, text="x  +").pack(side="left", padx=(6, 6))
        ctk.CTkEntry(self, textvariable=self._a2, width=60, justify="right").pack(side="left")
        ctk.CTkLabel(self, text="y").pack(side="left", padx=(6, 6))
        ctk.CTkOptionMenu(
            self,
            variable=self._op,
            values=list(self.OPERATORS),
            width=60,
        ).pack(side="left", padx=(0, 6))
        ctk.CTkEntry(self, textvariable=self._b, width=70, justify="right").pack(side="left")
        ctk.CTkButton(
            self,
            text="X",
            width=30,
            fg_color="#c62828",
            hover_color="#8e0000",
            command=self._delete_self,
        ).pack(side="left", padx=(10, 0))

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
