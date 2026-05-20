"""Ventana modal con la explicacion paso a paso del metodo grafico aplicado."""

from __future__ import annotations

import customtkinter as ctk

from src.application.dto.explanation_step import ExplanationStep


class ExplanationDialog(ctk.CTkToplevel):
    def __init__(self, parent, steps: list[ExplanationStep]) -> None:
        super().__init__(parent)
        self._steps = steps
        self._idx = 0

        self.title("Explicacion paso a paso")
        self.geometry("820x640")
        self.minsize(720, 540)
        self.transient(parent)
        self.grab_set()
        self.after(120, self._center_over_parent, parent)

        self._build()
        self._refresh()

    def _center_over_parent(self, parent) -> None:
        try:
            self.update_idletasks()
            px = parent.winfo_rootx()
            py = parent.winfo_rooty()
            pw = parent.winfo_width()
            ph = parent.winfo_height()
            w = self.winfo_width()
            h = self.winfo_height()
            x = px + (pw - w) // 2
            y = py + (ph - h) // 2
            self.geometry(f"+{x}+{y}")
        except Exception:
            pass

    def _build(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Indicador de paso
        self._step_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("#1565c0", "#64b5f6"),
        )
        self._step_label.grid(row=0, column=0, sticky="w", padx=20, pady=(16, 0))

        # Titulo
        self._title_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w",
            justify="left",
            wraplength=760,
        )
        self._title_label.grid(row=1, column=0, sticky="ew", padx=20, pady=(2, 12))

        # Contenido (textbox solo lectura, monoespaciada)
        self._textbox = ctk.CTkTextbox(
            self,
            wrap="none",
            font=ctk.CTkFont(family="Consolas", size=12),
            corner_radius=10,
        )
        self._textbox.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 12))

        # Botones de navegacion
        nav = ctk.CTkFrame(self, fg_color="transparent")
        nav.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 16))
        nav.grid_columnconfigure(1, weight=1)

        self._prev_btn = ctk.CTkButton(
            nav,
            text="< Anterior",
            width=140,
            command=self._on_prev,
            fg_color="transparent",
            border_width=2,
            text_color=("#37474f", "#cfd8dc"),
        )
        self._prev_btn.grid(row=0, column=0, sticky="w")

        self._close_btn = ctk.CTkButton(
            nav,
            text="Cerrar",
            width=110,
            command=self.destroy,
            fg_color="transparent",
            border_width=2,
            text_color=("#37474f", "#cfd8dc"),
        )
        self._close_btn.grid(row=0, column=1)

        self._next_btn = ctk.CTkButton(
            nav,
            text="Siguiente >",
            width=140,
            command=self._on_next,
            font=ctk.CTkFont(weight="bold"),
        )
        self._next_btn.grid(row=0, column=2, sticky="e")

    def _refresh(self) -> None:
        step = self._steps[self._idx]
        total = len(self._steps)
        self._step_label.configure(text=f"PASO {self._idx + 1} DE {total}")
        self._title_label.configure(text=step.title)

        self._textbox.configure(state="normal")
        self._textbox.delete("1.0", "end")
        self._textbox.insert("1.0", step.content)
        self._textbox.configure(state="disabled")

        self._prev_btn.configure(state=("disabled" if self._idx == 0 else "normal"))
        if self._idx == total - 1:
            self._next_btn.configure(text="Finalizar", command=self.destroy)
        else:
            self._next_btn.configure(text="Siguiente >", command=self._on_next)

    def _on_prev(self) -> None:
        if self._idx > 0:
            self._idx -= 1
            self._refresh()

    def _on_next(self) -> None:
        if self._idx < len(self._steps) - 1:
            self._idx += 1
            self._refresh()
