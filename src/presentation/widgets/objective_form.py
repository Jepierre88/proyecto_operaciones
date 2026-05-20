"""Widget para capturar la funcion objetivo (CustomTkinter)."""

from __future__ import annotations

import customtkinter as ctk


class ObjectiveForm(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, corner_radius=10)
        self._type_var = ctk.StringVar(value="max")
        self._c1_var = ctk.StringVar(value="3")
        self._c2_var = ctk.StringVar(value="5")
        self._build()

    def _build(self) -> None:
        ctk.CTkLabel(
            self, text="Funcion Objetivo", font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, columnspan=4, sticky="w", padx=14, pady=(12, 8))

        radios = ctk.CTkFrame(self, fg_color="transparent")
        radios.grid(row=1, column=0, columnspan=4, sticky="w", padx=14, pady=(0, 8))
        ctk.CTkRadioButton(
            radios, text="Maximizar", variable=self._type_var, value="max"
        ).pack(side="left", padx=(0, 16))
        ctk.CTkRadioButton(
            radios, text="Minimizar", variable=self._type_var, value="min"
        ).pack(side="left")

        ctk.CTkLabel(self, text="Z =").grid(row=2, column=0, padx=(14, 4), pady=(0, 14))
        ctk.CTkEntry(self, textvariable=self._c1_var, width=70, justify="right").grid(
            row=2, column=1, pady=(0, 14)
        )
        ctk.CTkLabel(self, text="x  +").grid(row=2, column=2, padx=(6, 6), pady=(0, 14))
        ctk.CTkEntry(self, textvariable=self._c2_var, width=70, justify="right").grid(
            row=2, column=3, pady=(0, 14)
        )
        ctk.CTkLabel(self, text="y").grid(row=2, column=4, padx=(6, 14), pady=(0, 14))

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
