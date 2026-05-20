"""Traduce LPSolution + LPProblem (dominio) -> SolutionResponse (DTO plano)."""

from __future__ import annotations

from src.application.dto.solution_response import SolutionResponse, VertexRow
from src.domain.entities.lp_problem import LPProblem
from src.domain.entities.lp_solution import LPSolution
from src.domain.entities.vertex import Vertex


class SolutionMapper:
    @staticmethod
    def to_response(solution: LPSolution, problem: LPProblem) -> SolutionResponse:
        vertex_rows = [
            SolutionMapper._row_from_vertex(v, is_optimal=SolutionMapper._is_optimal(v, solution))
            for v in solution.all_vertices
        ]
        vertex_rows.sort(key=lambda r: (r.x, r.y))

        optimal = solution.optimal_vertex
        return SolutionResponse(
            status=solution.status.value,
            status_description=solution.status.description_es,
            problem_name=problem.name,
            objective_text=problem.objective.as_pretty_string(),
            constraints_text=[c.as_pretty_string() for c in problem.constraints],
            optimal_x=optimal.x if optimal else None,
            optimal_y=optimal.y if optimal else None,
            optimal_z=solution.optimal_z,
            vertices=vertex_rows,
            has_alternative_optima=bool(solution.alternative_optima),
            message=solution.message,
        )

    @staticmethod
    def _row_from_vertex(vertex: Vertex, is_optimal: bool) -> VertexRow:
        active_text = ", ".join(
            c.label or c.as_pretty_string() for c in vertex.active_constraints
        )
        return VertexRow(
            x=vertex.x,
            y=vertex.y,
            z=vertex.z_value,
            is_optimal=is_optimal,
            active_constraints_text=active_text,
        )

    @staticmethod
    def _is_optimal(vertex: Vertex, solution: LPSolution) -> bool:
        if solution.optimal_vertex is None:
            return False
        if vertex.point.is_close_to(solution.optimal_vertex.point):
            return True
        return any(vertex.point.is_close_to(alt.point) for alt in solution.alternative_optima)
