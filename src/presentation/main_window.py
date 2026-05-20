"""Ventana principal con CustomTkinter."""

from __future__ import annotations

import tkinter as tk

import customtkinter as ctk

from src.application.dto.problem_request import ConstraintRequest, ProblemRequest
from src.presentation.controllers.main_controller import MainController
from src.presentation.widgets.constraints_list import ConstraintsList
from src.presentation.widgets.objective_form import ObjectiveForm
from src.presentation.widgets.plot_canvas import PlotCanvas
from src.presentation.widgets.results_panel import ResultsPanel
from src.presentation.widgets.status_bar import StatusBar

DEFAULT_PROBLEM_NAME = "Problema personalizado"


class MainWindow(ctk.CTk):
    def __init__(self, controller: MainController) -> None:
        super().__init__()
        self._controller = controller
        self._controller.bind_view(self)
        self._current_problem_name: str = DEFAULT_PROBLEM_NAME

        self.title("Programacion Lineal - Metodo Grafico (Linea A)")
        self.geometry("1280x800")
        self.minsize(1100, 680)

        self._build_toolbar()
        self._build_body()
        self._build_status_bar()
        self._populate_defaults()

    # --- construccion ---

    def _build_toolbar(self) -> None:
        bar = ctk.CTkFrame(self, height=56, corner_radius=0, fg_color=("#e8eaed", "#1a1d22"))
        bar.pack(side="top", fill="x")

        title = ctk.CTkLabel(
            bar,
            text="Programacion Lineal - Metodo Grafico",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        title.pack(side="left", padx=18, pady=10)

        # Boton Casos
        ctk.CTkButton(
            bar,
            text="Casos de prueba",
            width=140,
            command=self._open_samples_menu,
        ).pack(side="right", padx=(6, 14), pady=10)

        # Boton Archivo
        ctk.CTkButton(
            bar,
            text="Archivo",
            width=100,
            command=self._open_file_menu,
        ).pack(side="right", padx=6, pady=10)

        # Toggle de tema
        self._theme_var = ctk.StringVar(value="System")
        theme_menu = ctk.CTkOptionMenu(
            bar,
            values=["Light", "Dark", "System"],
            variable=self._theme_var,
            command=self._on_theme_change,
            width=110,
        )
        theme_menu.pack(side="right", padx=6, pady=10)
        ctk.CTkLabel(bar, text="Tema:").pack(side="right", padx=(12, 4), pady=10)

    def _build_body(self) -> None:
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=16, pady=16)

        body.grid_columnconfigure(0, weight=2, minsize=380)
        body.grid_columnconfigure(1, weight=3, minsize=600)
        body.grid_rowconfigure(0, weight=1)

        # --- IZQUIERDA: entrada ---
        left = ctk.CTkFrame(body, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left.grid_rowconfigure(1, weight=1)
        left.grid_columnconfigure(0, weight=1)

        self.objective_form = ObjectiveForm(left)
        self.objective_form.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.constraints_list = ConstraintsList(left)
        self.constraints_list.grid(row=1, column=0, sticky="nsew", pady=(0, 10))

        actions = ctk.CTkFrame(left, fg_color="transparent")
        actions.grid(row=2, column=0, sticky="ew")

        ctk.CTkButton(
            actions,
            text="Resolver",
            command=self._controller.on_solve,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(side="left", expand=True, fill="x", padx=(0, 4))
        ctk.CTkButton(
            actions,
            text="Limpiar",
            command=self._controller.on_clear,
            fg_color="transparent",
            border_width=2,
            text_color=("#37474f", "#cfd8dc"),
            height=40,
        ).pack(side="left", expand=True, fill="x", padx=4)
        ctk.CTkButton(
            actions,
            text="Exportar",
            command=self._controller.on_export_results,
            fg_color="#388e3c",
            hover_color="#1b5e20",
            height=40,
        ).pack(side="left", expand=True, fill="x", padx=(4, 0))

        # --- DERECHA: salida ---
        right = ctk.CTkFrame(body, fg_color="transparent")
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(0, weight=3)
        right.grid_rowconfigure(1, weight=2)

        self.plot_canvas = PlotCanvas(right)
        self.plot_canvas.grid(row=0, column=0, sticky="nsew", pady=(0, 8))

        self.results_panel = ResultsPanel(right)
        self.results_panel.grid(row=1, column=0, sticky="nsew")

    def _build_status_bar(self) -> None:
        self.status_bar = StatusBar(self)
        self.status_bar.pack(side="bottom", fill="x")

    def _populate_defaults(self) -> None:
        try:
            self._controller.on_load_sample("fabrica_muebles")
        except Exception:
            self._fallback_default()

    def _fallback_default(self) -> None:
        self.objective_form.set_values("max", 3, 5)
        self.constraints_list.clear()
        self.constraints_list.add_row(a1=1, a2=0, op="<=", b=4)
        self.constraints_list.add_row(a1=0, a2=2, op="<=", b=12)
        self.constraints_list.add_row(a1=3, a2=2, op="<=", b=18)

    # --- menus emergentes ---

    def _open_file_menu(self) -> None:
        menu = tk.Menu(self, tearoff=False)
        menu.add_command(label="Cargar problema...", command=self._controller.on_load_file)
        menu.add_command(label="Guardar problema...", command=self._controller.on_save_problem)
        menu.add_separator()
        menu.add_command(
            label="Descargar plantilla Excel...",
            command=self._controller.on_download_excel_template,
        )
        menu.add_separator()
        menu.add_command(
            label="Exportar resultados...", command=self._controller.on_export_results
        )
        menu.add_separator()
        menu.add_command(label="Salir", command=self.destroy)
        self._popup_under_cursor(menu)

    def _open_samples_menu(self) -> None:
        menu = tk.Menu(self, tearoff=False)
        for sample_id, display_name in self._controller.list_samples():
            menu.add_command(
                label=display_name,
                command=lambda sid=sample_id: self._controller.on_load_sample(sid),
            )
        self._popup_under_cursor(menu)

    def _popup_under_cursor(self, menu: tk.Menu) -> None:
        try:
            menu.tk_popup(self.winfo_pointerx(), self.winfo_pointery())
        finally:
            menu.grab_release()

    def _on_theme_change(self, value: str) -> None:
        ctk.set_appearance_mode(value.lower())

    # --- API para el controller ---

    def collect_problem_request(self) -> ProblemRequest:
        objective_type, c1, c2 = self.objective_form.get_values()
        raw_constraints = self.constraints_list.get_values()
        if not raw_constraints:
            raise ValueError("Agrega al menos una restriccion antes de resolver.")
        constraints = [
            ConstraintRequest(a1=a1, a2=a2, operator=op, b=b)
            for (a1, a2, op, b) in raw_constraints
        ]
        return ProblemRequest(
            objective_type=objective_type,
            c1=c1,
            c2=c2,
            constraints=constraints,
            name=self._current_problem_name,
        )

    def apply_problem_request(self, request: ProblemRequest) -> None:
        self._current_problem_name = request.name or DEFAULT_PROBLEM_NAME
        self.objective_form.set_values(request.objective_type, request.c1, request.c2)
        self.constraints_list.set_from_requests(request.constraints)
        self.results_panel.clear()
        self.title(f"Programacion Lineal - {self._current_problem_name}")

    def reset(self) -> None:
        self._current_problem_name = DEFAULT_PROBLEM_NAME
        self.objective_form.set_values("max", 1, 1)
        self.constraints_list.clear()
        self.results_panel.clear()
        self.title("Programacion Lineal - Metodo Grafico (Linea A)")
