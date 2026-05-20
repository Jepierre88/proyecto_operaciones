"""Ventana principal: ensambla widgets y delega eventos al controller."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from src.application.dto.problem_request import ConstraintRequest, ProblemRequest
from src.presentation.controllers.main_controller import MainController
from src.presentation.widgets.constraints_list import ConstraintsList
from src.presentation.widgets.objective_form import ObjectiveForm
from src.presentation.widgets.plot_canvas import PlotCanvas
from src.presentation.widgets.results_panel import ResultsPanel
from src.presentation.widgets.status_bar import StatusBar

DEFAULT_PROBLEM_NAME = "Problema personalizado"


class MainWindow(tk.Tk):
    def __init__(self, controller: MainController) -> None:
        super().__init__()
        self._controller = controller
        self._controller.bind_view(self)
        self._current_problem_name: str = DEFAULT_PROBLEM_NAME

        self.title("Programacion Lineal - Metodo Grafico (Linea A)")
        self.geometry("1180x760")
        self.minsize(1000, 640)

        self._build_menu()
        self._build_body()
        self._build_status_bar()
        self._populate_defaults()

    # --- construccion ---

    def _build_menu(self) -> None:
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="Cargar problema...", command=self._controller.on_load_file)
        file_menu.add_command(label="Guardar problema...", command=self._controller.on_save_problem)
        file_menu.add_separator()
        file_menu.add_command(
            label="Exportar resultados...", command=self._controller.on_export_results
        )
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.destroy)
        menubar.add_cascade(label="Archivo", menu=file_menu)

        samples_menu = tk.Menu(menubar, tearoff=False)
        for sample_id, display_name in self._controller.list_samples():
            samples_menu.add_command(
                label=display_name,
                command=lambda sid=sample_id: self._controller.on_load_sample(sid),
            )
        menubar.add_cascade(label="Casos de prueba", menu=samples_menu)

        self.config(menu=menubar)

    def _build_body(self) -> None:
        paned = ttk.PanedWindow(self, orient="horizontal")
        paned.pack(fill="both", expand=True, padx=8, pady=8)

        left = ttk.Frame(paned)
        right = ttk.Frame(paned)
        paned.add(left, weight=1)
        paned.add(right, weight=2)

        # --- IZQUIERDA: entrada ---
        self.objective_form = ObjectiveForm(left)
        self.objective_form.pack(fill="x", pady=(0, 8))

        self.constraints_list = ConstraintsList(left)
        self.constraints_list.pack(fill="both", expand=True, pady=(0, 8))

        actions = ttk.Frame(left)
        actions.pack(fill="x")
        ttk.Button(actions, text="Resolver", command=self._controller.on_solve).pack(
            side="left", padx=(0, 6)
        )
        ttk.Button(actions, text="Limpiar", command=self._controller.on_clear).pack(
            side="left", padx=(0, 6)
        )
        ttk.Button(
            actions, text="Exportar resultados", command=self._controller.on_export_results
        ).pack(side="left")

        # --- DERECHA: salida ---
        right_paned = ttk.PanedWindow(right, orient="vertical")
        right_paned.pack(fill="both", expand=True)

        plot_frame = ttk.LabelFrame(right_paned, text="Region factible", padding=4)
        self.plot_canvas = PlotCanvas(plot_frame)
        self.plot_canvas.pack(fill="both", expand=True)
        right_paned.add(plot_frame, weight=3)

        self.results_panel = ResultsPanel(right_paned)
        right_paned.add(self.results_panel, weight=2)

    def _build_status_bar(self) -> None:
        self.status_bar = StatusBar(self)
        self.status_bar.pack(side="bottom", fill="x")

    def _populate_defaults(self) -> None:
        # Carga por defecto el caso de la fabrica para facilitar la demo
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
