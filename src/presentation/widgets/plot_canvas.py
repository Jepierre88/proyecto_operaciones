"""Embebe una matplotlib.Figure dentro de un CTkFrame con toolbar."""

from __future__ import annotations

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


class PlotCanvas(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, corner_radius=10)
        # Importante: no usar nombres como _canvas o _toolbar, que CTkFrame usa internamente.
        self._figure_canvas: FigureCanvasTkAgg | None = None
        self._mpl_toolbar: NavigationToolbar2Tk | None = None
        self._toolbar_frame: ctk.CTkFrame | None = None
        self._placeholder: ctk.CTkLabel | None = ctk.CTkLabel(
            self,
            text="El grafico aparecera aqui despues de resolver",
            font=ctk.CTkFont(size=13, slant="italic"),
            text_color=("#666", "#aaa"),
        )
        self._placeholder.pack(fill="both", expand=True, padx=20, pady=20)

    def render(self, figure: Figure) -> None:
        self._clear_content()
        self._figure_canvas = FigureCanvasTkAgg(figure, master=self)
        self._figure_canvas.draw()

        self._toolbar_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self._toolbar_frame.pack(side="bottom", fill="x")
        self._mpl_toolbar = NavigationToolbar2Tk(
            self._figure_canvas, self._toolbar_frame, pack_toolbar=False
        )
        self._mpl_toolbar.update()
        self._mpl_toolbar.pack(side="left")

        self._figure_canvas.get_tk_widget().pack(
            side="top", fill="both", expand=True, padx=8, pady=(8, 0)
        )

    def _clear_content(self) -> None:
        if self._placeholder is not None:
            self._placeholder.destroy()
            self._placeholder = None
        if self._mpl_toolbar is not None:
            self._mpl_toolbar.destroy()
            self._mpl_toolbar = None
        if self._toolbar_frame is not None:
            self._toolbar_frame.destroy()
            self._toolbar_frame = None
        if self._figure_canvas is not None:
            self._figure_canvas.get_tk_widget().destroy()
            self._figure_canvas = None
