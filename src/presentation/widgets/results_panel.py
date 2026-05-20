"""Panel de resultados: estado + optimo + tabla custom (CustomTkinter)."""

from __future__ import annotations

import customtkinter as ctk

from src.application.dto.solution_response import SolutionResponse


COLUMNS = (
    ("x", 70, "e"),
    ("y", 70, "e"),
    ("Z", 90, "e"),
    ("Restricciones activas", 300, "w"),
)


class ResultsPanel(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, corner_radius=10)
        self._status_var = ctk.StringVar(value="(sin resolver)")
        self._optimum_var = ctk.StringVar(value="")
        self._row_widgets: list[ctk.CTkBaseClass] = []
        self._build()

    def _build(self) -> None:
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=14, pady=(12, 4))
        ctk.CTkLabel(
            header, text="Resultados", font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            self, textvariable=self._status_var, font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=14, pady=(2, 0))
        ctk.CTkLabel(
            self,
            textvariable=self._optimum_var,
            text_color=("#1565c0", "#64b5f6"),
            font=ctk.CTkFont(size=13, weight="bold"),
        ).pack(anchor="w", padx=14, pady=(0, 8))

        # Encabezado de la tabla
        self._table_header = ctk.CTkFrame(self, fg_color=("#1565c0", "#0d47a1"), corner_radius=6)
        self._table_header.pack(fill="x", padx=14, pady=(0, 2))
        for title, width, anchor in COLUMNS:
            ctk.CTkLabel(
                self._table_header,
                text=title,
                width=width,
                anchor=anchor,
                text_color="white",
                font=ctk.CTkFont(weight="bold"),
            ).pack(side="left", padx=4, pady=4)

        self._table_body = ctk.CTkScrollableFrame(self, fg_color="transparent", height=220)
        self._table_body.pack(fill="both", expand=True, padx=14, pady=(0, 12))

    def show(self, response: SolutionResponse) -> None:
        self._status_var.set(f"Estado: {response.status_description}")
        if response.optimal_x is not None:
            opt = (
                f"Punto optimo: ({response.optimal_x:g}, {response.optimal_y:g})"
                f"    Z = {response.optimal_z:g}"
            )
            if response.has_alternative_optima:
                opt += "   (multiples soluciones optimas)"
            self._optimum_var.set(opt)
        else:
            self._optimum_var.set(response.message or "")

        self._clear_rows()
        for idx, row in enumerate(response.vertices):
            self._add_row(idx, row.x, row.y, row.z, row.is_optimal, row.active_constraints_text)

    def _add_row(
        self,
        index: int,
        x: float,
        y: float,
        z: float,
        is_optimal: bool,
        active_text: str,
    ) -> None:
        if is_optimal:
            bg = ("#fff3e0", "#3e2723")
            font = ctk.CTkFont(weight="bold")
            text_color = ("#bf360c", "#ffab91")
            z_text = f"{z:g} *"
        else:
            bg = ("#f5f5f5", "#1e1e1e") if index % 2 == 0 else ("#ffffff", "#2a2a2a")
            font = ctk.CTkFont()
            text_color = None
            z_text = f"{z:g}"

        row_frame = ctk.CTkFrame(self._table_body, fg_color=bg, corner_radius=4)
        row_frame.pack(fill="x", pady=1)
        self._row_widgets.append(row_frame)

        cells = [
            (f"{x:g}", COLUMNS[0][1], COLUMNS[0][2]),
            (f"{y:g}", COLUMNS[1][1], COLUMNS[1][2]),
            (z_text, COLUMNS[2][1], COLUMNS[2][2]),
            (active_text, COLUMNS[3][1], COLUMNS[3][2]),
        ]
        for text, width, anchor in cells:
            kwargs = {"text": text, "width": width, "anchor": anchor, "font": font}
            if text_color is not None:
                kwargs["text_color"] = text_color
            ctk.CTkLabel(row_frame, **kwargs).pack(side="left", padx=4, pady=4)

    def _clear_rows(self) -> None:
        for w in self._row_widgets:
            w.destroy()
        self._row_widgets.clear()

    def clear(self) -> None:
        self._status_var.set("(sin resolver)")
        self._optimum_var.set("")
        self._clear_rows()
