"""Traduce ProblemRequest (DTO plano) -> LPProblem (dominio). Aqui vive la validacion."""

from __future__ import annotations

from src.application.dto.problem_request import ProblemRequest
from src.domain.entities.constraint import Constraint
from src.domain.entities.lp_problem import LPProblem
from src.domain.entities.objective import Objective
from src.domain.value_objects.operator import Operator
from src.domain.value_objects.optimization_type import OptimizationType


class ProblemValidationError(ValueError):
    pass


class ProblemMapper:
    @staticmethod
    def to_domain(request: ProblemRequest) -> LPProblem:
        try:
            opt_type = OptimizationType.from_string(request.objective_type)
        except ValueError as exc:
            raise ProblemValidationError(str(exc)) from exc

        if request.c1 == 0 and request.c2 == 0:
            raise ProblemValidationError(
                "La funcion objetivo no puede tener ambos coeficientes en cero"
            )

        if not request.constraints:
            raise ProblemValidationError("El problema debe tener al menos una restriccion")

        objective = Objective(
            c1=float(request.c1), c2=float(request.c2), optimization_type=opt_type
        )

        constraints: list[Constraint] = []
        for idx, c in enumerate(request.constraints, start=1):
            try:
                op = Operator.from_symbol(c.operator)
            except ValueError as exc:
                raise ProblemValidationError(f"Restriccion #{idx}: {exc}") from exc
            try:
                constraints.append(
                    Constraint(
                        a1=float(c.a1),
                        a2=float(c.a2),
                        operator=op,
                        b=float(c.b),
                        label=c.label or f"R{idx}",
                    )
                )
            except ValueError as exc:
                raise ProblemValidationError(f"Restriccion #{idx}: {exc}") from exc

        return LPProblem(
            objective=objective,
            constraints=tuple(constraints),
            name=request.name or "Problema sin nombre",
        )
