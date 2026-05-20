"""Embebe una matplotlib.Figure dentro de un Frame Tkinter con toolbar."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


class PlotCanvas(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self._canvas: FigureCanvasTkAgg | None = None
        self._toolbar: NavigationToolbar2Tk | None = None
        self._placeholder = ttk.Label(
            self,
            text="(El grafico aparecera aqui despues de resolver)",
            anchor="center",
            foreground="#666",
        )
        self._placeholder.pack(fill="both", expand=True)

    def render(self, figure: Figure) -> None:
        self._clear()
        self._canvas = FigureCanvasTkAgg(figure, master=self)
        self._canvas.draw()
        toolbar_frame = ttk.Frame(self)
        toolbar_frame.pack(side="bottom", fill="x")
        self._toolbar = NavigationToolbar2Tk(self._canvas, toolbar_frame)
        self._toolbar.update()
        self._canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    def _clear(self) -> None:
        if self._placeholder is not None:
            self._placeholder.destroy()
            self._placeholder = None
        if self._toolbar is not None:
            self._toolbar.destroy()
            self._toolbar = None
        if self._canvas is not None:
            self._canvas.get_tk_widget().destroy()
            self._canvas = None
        for child in self.winfo_children():
            child.destroy()
