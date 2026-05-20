"""Genera un PDF de una pagina con el problema, grafico, tabla y analisis."""

from __future__ import annotations

import tempfile
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from src.application.dto.solution_response import SolutionResponse
from src.domain.entities.lp_problem import LPProblem
from src.domain.entities.lp_solution import LPSolution
from src.infrastructure.plotting.feasible_region_plotter import (
    MatplotlibFeasibleRegionPlotter,
)


class PdfReportGenerator:
    def __init__(self, plotter: MatplotlibFeasibleRegionPlotter) -> None:
        self._plotter = plotter

    def export_pdf(
        self,
        response: SolutionResponse,
        problem: LPProblem,
        solution: LPSolution,
        path: Path,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            chart_path = Path(tmp) / "_chart.png"
            self._plotter.export_png(problem, solution, chart_path)

            doc = SimpleDocTemplate(
                str(path),
                pagesize=A4,
                leftMargin=1.5 * cm,
                rightMargin=1.5 * cm,
                topMargin=1.5 * cm,
                bottomMargin=1.5 * cm,
                title=f"Informe PL - {response.problem_name}",
            )
            story = list(self._build_story(response, chart_path))
            doc.build(story)

    def _build_story(self, response: SolutionResponse, chart_path: Path):
        styles = getSampleStyleSheet()
        h1 = ParagraphStyle(
            "H1", parent=styles["Heading1"], fontSize=14, spaceAfter=8, textColor=colors.HexColor("#1565c0")
        )
        h2 = ParagraphStyle(
            "H2", parent=styles["Heading2"], fontSize=11, spaceAfter=4, textColor=colors.HexColor("#37474f")
        )
        body = styles["BodyText"]

        yield Paragraph(f"Investigacion de Operaciones - Linea A", h1)
        yield Paragraph(f"<b>Problema:</b> {response.problem_name}", body)
        yield Paragraph(f"<b>Funcion objetivo:</b> {response.objective_text}", body)
        yield Spacer(1, 0.2 * cm)

        yield Paragraph("Restricciones", h2)
        for text in response.constraints_text:
            yield Paragraph(f"&bull; {text}", body)
        yield Spacer(1, 0.3 * cm)

        yield Paragraph("Region factible", h2)
        yield Image(str(chart_path), width=15 * cm, height=11 * cm)
        yield Spacer(1, 0.3 * cm)

        yield Paragraph("Resultado", h2)
        yield Paragraph(f"<b>Estado:</b> {response.status_description}", body)
        if response.optimal_x is not None:
            yield Paragraph(
                f"<b>Punto optimo:</b> x = {response.optimal_x:g}, y = {response.optimal_y:g}",
                body,
            )
            yield Paragraph(f"<b>Valor optimo de Z:</b> {response.optimal_z:g}", body)
        if response.has_alternative_optima:
            yield Paragraph(
                "<i>Nota: el problema tiene multiples soluciones optimas (optimo alterno).</i>",
                body,
            )
        yield Spacer(1, 0.3 * cm)

        yield Paragraph("Tabla de vertices factibles", h2)
        table_data = [["x", "y", "Z", "Optimo", "Restricciones activas"]]
        for row in response.vertices:
            table_data.append(
                [
                    f"{row.x:g}",
                    f"{row.y:g}",
                    f"{row.z:g}",
                    "*" if row.is_optimal else "",
                    row.active_constraints_text,
                ]
            )
        table = Table(table_data, hAlign="LEFT", repeatRows=1)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1565c0")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                    ("ALIGN", (0, 0), (2, -1), "RIGHT"),
                    ("ALIGN", (3, 0), (3, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
                ]
            )
        )
        yield table
