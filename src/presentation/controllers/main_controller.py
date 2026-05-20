"""Coordina UI y casos de uso. No contiene matematica."""

from __future__ import annotations

from pathlib import Path
from tkinter import filedialog, messagebox

from src.application.dto.problem_request import ConstraintRequest, ProblemRequest
from src.application.mappers.problem_mapper import ProblemValidationError
from src.application.use_cases.export_results import ExportResultsUseCase
from src.application.use_cases.load_problem_from_file import LoadProblemFromFileUseCase
from src.application.use_cases.load_sample_problem import LoadSampleProblemUseCase
from src.application.use_cases.solve_lp_problem import SolveLPProblemUseCase, SolveResult
from src.infrastructure.persistence.json_problem_loader import JsonProblemLoader
from src.infrastructure.plotting.feasible_region_plotter import (
    MatplotlibFeasibleRegionPlotter,
)


class MainController:
    def __init__(
        self,
        solve_uc: SolveLPProblemUseCase,
        load_file_uc: LoadProblemFromFileUseCase,
        load_sample_uc: LoadSampleProblemUseCase,
        export_uc: ExportResultsUseCase,
        plotter: MatplotlibFeasibleRegionPlotter,
        json_loader: JsonProblemLoader,
    ) -> None:
        self._solve = solve_uc
        self._load_file = load_file_uc
        self._load_sample = load_sample_uc
        self._export = export_uc
        self._plotter = plotter
        self._json_loader = json_loader
        self._last_result: SolveResult | None = None
        self._view = None  # se inyecta despues

    def bind_view(self, view) -> None:
        self._view = view

    # --- acciones ---

    def on_solve(self) -> None:
        try:
            request = self._view.collect_problem_request()
        except ValueError as exc:
            self._view.status_bar.error(str(exc))
            return

        try:
            result = self._solve.execute(request)
        except ProblemValidationError as exc:
            self._view.status_bar.error(str(exc))
            messagebox.showerror("Problema invalido", str(exc))
            return

        self._last_result = result
        figure = self._plotter.build_figure(result.problem, result.solution)
        self._view.plot_canvas.render(figure)
        self._view.results_panel.show(result.response)
        self._view.status_bar.info(
            f"Resuelto: {result.response.status_description}."
        )

    def on_clear(self) -> None:
        self._view.reset()
        self._last_result = None
        self._view.status_bar.info("Formulario limpiado.")

    def on_load_file(self) -> None:
        path = filedialog.askopenfilename(
            title="Cargar problema",
            filetypes=[("JSON", "*.json"), ("CSV", "*.csv"), ("Todos", "*.*")],
        )
        if not path:
            return
        try:
            request = self._load_file.execute(path)
        except Exception as exc:
            messagebox.showerror("No se pudo cargar", str(exc))
            return
        self._view.apply_problem_request(request)
        self._view.status_bar.info(f"Problema cargado desde {Path(path).name}.")

    def on_load_sample(self, sample_id: str) -> None:
        try:
            request = self._load_sample.execute(sample_id)
        except KeyError as exc:
            messagebox.showerror("Caso no encontrado", str(exc))
            return
        self._view.apply_problem_request(request)
        self._view.status_bar.info(f"Caso precargado: {request.name}")

    def on_save_problem(self) -> None:
        try:
            request = self._view.collect_problem_request()
        except ValueError as exc:
            self._view.status_bar.error(str(exc))
            return
        path = filedialog.asksaveasfilename(
            title="Guardar problema",
            defaultextension=".json",
            filetypes=[("JSON", "*.json")],
        )
        if not path:
            return
        self._json_loader.save(request, Path(path))
        self._view.status_bar.info(f"Problema guardado en {Path(path).name}.")

    def on_export_results(self) -> None:
        if self._last_result is None:
            messagebox.showinfo(
                "Sin resultados", "Primero resuelve el problema para exportar resultados."
            )
            return
        out_dir = filedialog.askdirectory(title="Carpeta de salida para los resultados")
        if not out_dir:
            return
        base_name = self._safe_filename(self._last_result.problem.name)
        result = self._export.execute(
            response=self._last_result.response,
            problem=self._last_result.problem,
            solution=self._last_result.solution,
            output_dir=out_dir,
            base_name=base_name,
        )
        names = "\n".join(str(p) for p in result.files)
        messagebox.showinfo("Exportacion completa", f"Archivos generados:\n{names}")
        self._view.status_bar.info(f"Exportados {len(result.files)} archivos.")

    def list_samples(self) -> list[tuple[str, str]]:
        return self._load_sample.list()

    @staticmethod
    def _safe_filename(name: str) -> str:
        safe = "".join(ch if ch.isalnum() or ch in ("_", "-") else "_" for ch in name)
        return safe.strip("_") or "resultado_pl"
