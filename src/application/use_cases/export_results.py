"""Caso de uso: exportar resultados a PNG (grafico), CSV (tabla) y PDF (reporte)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from src.application.dto.solution_response import SolutionResponse
from src.domain.entities.lp_problem import LPProblem
from src.domain.entities.lp_solution import LPSolution


class FigureExporter(Protocol):
    def export_png(self, problem: LPProblem, solution: LPSolution, path: Path) -> None: ...


class TableExporter(Protocol):
    def export_csv(self, response: SolutionResponse, path: Path) -> None: ...


class ReportExporter(Protocol):
    def export_pdf(
        self, response: SolutionResponse, problem: LPProblem, solution: LPSolution, path: Path
    ) -> None: ...


@dataclass(frozen=True)
class ExportOptions:
    include_png: bool = True
    include_csv: bool = True
    include_pdf: bool = True


@dataclass(frozen=True)
class ExportResult:
    files: list[Path]


class ExportResultsUseCase:
    def __init__(
        self,
        figure_exporter: FigureExporter,
        table_exporter: TableExporter,
        report_exporter: ReportExporter,
    ) -> None:
        self._figure = figure_exporter
        self._table = table_exporter
        self._report = report_exporter

    def execute(
        self,
        response: SolutionResponse,
        problem: LPProblem,
        solution: LPSolution,
        output_dir: str | Path,
        base_name: str = "resultado_pl",
        options: ExportOptions = ExportOptions(),
    ) -> ExportResult:
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        files: list[Path] = []

        if options.include_png:
            target = out_dir / f"{base_name}.png"
            self._figure.export_png(problem, solution, target)
            files.append(target)

        if options.include_csv:
            target = out_dir / f"{base_name}.csv"
            self._table.export_csv(response, target)
            files.append(target)

        if options.include_pdf:
            target = out_dir / f"{base_name}.pdf"
            self._report.export_pdf(response, problem, solution, target)
            files.append(target)

        return ExportResult(files=files)
