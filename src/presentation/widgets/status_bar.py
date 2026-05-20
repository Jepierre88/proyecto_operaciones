"""Barra inferior para mensajes (CustomTkinter)."""

from __future__ import annotations

import customtkinter as ctk


class StatusBar(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, height=28, corner_radius=0)
        self._text_var = ctk.StringVar(value="Listo.")
        self._label = ctk.CTkLabel(
            self,
            textvariable=self._text_var,
            anchor="w",
            font=ctk.CTkFont(size=12),
        )
        self._label.pack(fill="x", padx=12, pady=4)

    def info(self, message: str) -> None:
        self._text_var.set(message)
        self._label.configure(text_color=("#2e7d32", "#81c784"))

    def error(self, message: str) -> None:
        self._text_var.set(f"ERROR: {message}")
        self._label.configure(text_color=("#c62828", "#ef9a9a"))
