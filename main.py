"""Entry point - Composition Root.

Aqui se instancian y se conectan TODAS las dependencias entre capas.
Es el unico archivo que conoce todas las capas a la vez.
"""

from __future__ import annotations

import customtkinter as ctk

from src.application.services.solution_explainer import SolutionExplainer
from src.application.use_cases.export_results import ExportResultsUseCase
from src.application.use_cases.load_problem_from_file import LoadProblemFromFileUseCase
from src.application.use_cases.load_sample_problem import LoadSampleProblemUseCase
from src.application.use_cases.solve_lp_problem import SolveLPProblemUseCase
from src.domain.services.feasibility_checker import FeasibilityChecker
from src.domain.services.optimal_solver import OptimalSolver
from src.domain.services.unboundedness_detector import UnboundednessDetector
from src.domain.services.vertex_calculator import VertexCalculator
from src.infrastructure.persistence.csv_problem_loader import CsvProblemLoader
from src.infrastructure.persistence.csv_results_exporter import CsvResultsExporter
from src.infrastructure.persistence.json_problem_loader import JsonProblemLoader
from src.infrastructure.persistence.pdf_report_generator import PdfReportGenerator
from src.infrastructure.persistence.xlsx_problem_loader import XlsxProblemLoader
from src.infrastructure.plotting.feasible_region_plotter import (
    MatplotlibFeasibleRegionPlotter,
)
from src.infrastructure.samples.sample_catalog import JsonSampleCatalog
from src.presentation.controllers.main_controller import MainController
from src.presentation.main_window import MainWindow


def build_app() -> MainWindow:
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    # Dominio
    feasibility = FeasibilityChecker()
    solver = OptimalSolver(
        vertex_calculator=VertexCalculator(),
        feasibility_checker=feasibility,
        unboundedness_detector=UnboundednessDetector(feasibility),
    )

    # Infraestructura
    plotter = MatplotlibFeasibleRegionPlotter()
    json_loader = JsonProblemLoader()
    csv_loader = CsvProblemLoader()
    xlsx_loader = XlsxProblemLoader()
    csv_exporter = CsvResultsExporter()
    pdf_generator = PdfReportGenerator(plotter)
    sample_catalog = JsonSampleCatalog()

    # Casos de uso
    solve_uc = SolveLPProblemUseCase(solver)
    load_file_uc = LoadProblemFromFileUseCase(loaders=[json_loader, csv_loader, xlsx_loader])
    load_sample_uc = LoadSampleProblemUseCase(sample_catalog)
    export_uc = ExportResultsUseCase(
        figure_exporter=plotter,
        table_exporter=csv_exporter,
        report_exporter=pdf_generator,
    )
    explainer = SolutionExplainer()

    # Presentacion
    controller = MainController(
        solve_uc=solve_uc,
        load_file_uc=load_file_uc,
        load_sample_uc=load_sample_uc,
        export_uc=export_uc,
        plotter=plotter,
        json_loader=json_loader,
        xlsx_loader=xlsx_loader,
        explainer=explainer,
    )
    return MainWindow(controller)


def main() -> None:
    app = build_app()
    app.mainloop()


if __name__ == "__main__":
    main()
