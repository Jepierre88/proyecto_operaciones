"""Barra inferior para mensajes informativos / errores no fatales."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class StatusBar(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, padding=(8, 4))
        self._text_var = tk.StringVar(value="Listo.")
        ttk.Label(self, textvariable=self._text_var, anchor="w").pack(fill="x")

    def info(self, message: str) -> None:
        self._text_var.set(message)

    def error(self, message: str) -> None:
        self._text_var.set(f"ERROR: {message}")
