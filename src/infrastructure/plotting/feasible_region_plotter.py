"""Grafica region factible, restricciones, vertices y optimo con matplotlib.

Devuelve una matplotlib.figure.Figure que la UI Tkinter embebe (FigureCanvasTkAgg)
o el exportador guarda con figure.savefig(). Una sola fuente de verdad.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
import numpy as np
from matplotlib.figure import Figure
from matplotlib.patches import Polygon as MplPolygon

from src.domain.entities.constraint import Constraint
from src.domain.entities.lp_problem import LPProblem
from src.domain.entities.lp_solution import LPSolution
from src.domain.value_objects.operator import Operator
from src.domain.value_objects.solution_status import SolutionStatus


class MatplotlibFeasibleRegionPlotter:
    """Construye la figura. No la muestra ni la guarda (eso lo decide quien llama)."""

    def __init__(self, dpi: int = 100) -> None:
        self._dpi = dpi

    def build_figure(self, problem: LPProblem, solution: LPSolution) -> Figure:
        figure = Figure(figsize=(7, 6), dpi=self._dpi)
        ax = figure.add_subplot(111)

        x_max, y_max = self._compute_axis_limits(solution)
        x_grid = np.linspace(0, x_max, 400)

        # Region factible (poligono sombreado)
        self._plot_feasible_region(ax, solution)

        # Cada restriccion como linea
        for idx, c in enumerate(problem.constraints):
            self._plot_constraint_line(ax, c, x_grid, y_max, label_idx=idx + 1)

        # Vertices factibles
        self._plot_vertices(ax, solution)

        # Punto optimo destacado
        if solution.optimal_vertex is not None:
            self._plot_optimal(ax, solution, x_grid, problem)

        # Mensaje de estado especial
        if solution.status is SolutionStatus.INFEASIBLE:
            ax.text(
                0.5,
                0.5,
                "REGION FACTIBLE VACIA\n(problema infactible)",
                transform=ax.transAxes,
                ha="center",
                va="center",
                fontsize=14,
                color="red",
                bbox={"boxstyle": "round", "facecolor": "white", "edgecolor": "red"},
            )
        elif solution.status is SolutionStatus.UNBOUNDED:
            ax.text(
                0.02,
                0.95,
                "PROBLEMA NO ACOTADO",
                transform=ax.transAxes,
                ha="left",
                va="top",
                fontsize=12,
                color="darkorange",
                bbox={"boxstyle": "round", "facecolor": "white", "edgecolor": "darkorange"},
            )

        ax.axhline(0, color="black", linewidth=0.6)
        ax.axvline(0, color="black", linewidth=0.6)
        ax.set_xlim(-x_max * 0.05, x_max)
        ax.set_ylim(-y_max * 0.05, y_max)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(problem.name)
        ax.grid(True, alpha=0.3)
        ax.legend(loc="best", fontsize=8)
        figure.tight_layout()
        return figure

    def _compute_axis_limits(self, solution: LPSolution) -> tuple[float, float]:
        if solution.all_vertices:
            xs = [v.x for v in solution.all_vertices]
            ys = [v.y for v in solution.all_vertices]
            x_max = max(xs + [1.0])
            y_max = max(ys + [1.0])
        else:
            x_max = y_max = 10.0
        margin = 1.2
        return x_max * margin, y_max * margin

    def _plot_constraint_line(
        self, ax, constraint: Constraint, x_grid: np.ndarray, y_max: float, label_idx: int
    ) -> None:
        label = constraint.label or f"R{label_idx}"
        full_label = f"{label}: {constraint.as_pretty_string()}"
        if constraint.a2 != 0:
            y_line = (constraint.b - constraint.a1 * x_grid) / constraint.a2
            ax.plot(x_grid, y_line, label=full_label, linewidth=1.5)
        elif constraint.a1 != 0:
            x_val = constraint.b / constraint.a1
            ax.plot(
                [x_val, x_val], [0, y_max], label=full_label, linewidth=1.5
            )

    def _plot_feasible_region(self, ax, solution: LPSolution) -> None:
        if len(solution.all_vertices) < 3:
            return
        points = np.array([(v.x, v.y) for v in solution.all_vertices])
        centroid = points.mean(axis=0)
        angles = np.arctan2(points[:, 1] - centroid[1], points[:, 0] - centroid[0])
        order = np.argsort(angles)
        ordered = points[order]
        polygon = MplPolygon(
            ordered,
            closed=True,
            facecolor="#a5d6a7",
            edgecolor="#2e7d32",
            alpha=0.45,
            linewidth=1.5,
            label="Region factible",
        )
        ax.add_patch(polygon)

    def _plot_vertices(self, ax, solution: LPSolution) -> None:
        for v in solution.all_vertices:
            ax.plot(v.x, v.y, "o", color="#1565c0", markersize=6, zorder=5)
            ax.annotate(
                f"({v.x:g}, {v.y:g})",
                xy=(v.x, v.y),
                xytext=(6, 6),
                textcoords="offset points",
                fontsize=8,
                color="#1565c0",
            )

    def _plot_optimal(
        self, ax, solution: LPSolution, x_grid: np.ndarray, problem: LPProblem
    ) -> None:
        opt = solution.optimal_vertex
        ax.plot(
            opt.x,
            opt.y,
            "*",
            color="#d32f2f",
            markersize=20,
            zorder=10,
            label=f"Optimo ({opt.x:g}, {opt.y:g}) Z={solution.optimal_z:g}",
        )
        # Linea de nivel de Z en el optimo (curva de indiferencia)
        c1, c2 = problem.objective.c1, problem.objective.c2
        if c2 != 0:
            y_line = (solution.optimal_z - c1 * x_grid) / c2
            ax.plot(
                x_grid,
                y_line,
                "--",
                color="#d32f2f",
                linewidth=1.2,
                alpha=0.7,
                label=f"Z = {solution.optimal_z:g}",
            )

    def export_png(self, problem: LPProblem, solution: LPSolution, path: Path) -> None:
        # Para export sin UI hay que forzar backend no interactivo
        matplotlib.use("Agg", force=False)
        figure = self.build_figure(problem, solution)
        figure.savefig(path, dpi=150, bbox_inches="tight")
