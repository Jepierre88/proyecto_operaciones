"""Genera la explicacion paso a paso del metodo grafico aplicado al problema actual.

Cada paso describe que se hizo, que formula se aplico y con que valores concretos
del problema que el usuario acaba de resolver.
"""

from __future__ import annotations

from math import comb

from src.application.dto.explanation_step import ExplanationStep
from src.domain.entities.lp_problem import LPProblem
from src.domain.entities.lp_solution import LPSolution
from src.domain.value_objects.operator import Operator
from src.domain.value_objects.optimization_type import OptimizationType
from src.domain.value_objects.solution_status import SolutionStatus


class SolutionExplainer:
    """Construye una lista de ExplanationStep para narrar la solucion."""

    def explain(self, problem: LPProblem, solution: LPSolution) -> list[ExplanationStep]:
        steps: list[ExplanationStep] = [
            self._step_modelo(problem),
            self._step_estrategia(problem),
            self._step_intersecciones(problem),
        ]

        if solution.status is SolutionStatus.INFEASIBLE:
            steps.append(self._step_infactible(problem))
            return steps

        steps.append(self._step_filtrado(problem, solution))
        steps.append(self._step_evaluacion(problem, solution))

        if solution.status is SolutionStatus.UNBOUNDED:
            steps.append(self._step_no_acotado(problem))
            return steps

        steps.append(self._step_seleccion(problem, solution))
        steps.append(self._step_restricciones_activas(problem, solution))
        return steps

    # -----------------------------------------------------------------
    # Paso 1: planteamiento del modelo
    # -----------------------------------------------------------------
    def _step_modelo(self, problem: LPProblem) -> ExplanationStep:
        objective = problem.objective
        verbo = "Maximizar" if objective.optimization_type is OptimizationType.MAX else "Minimizar"
        lines = [
            "MODELO DE PROGRAMACION LINEAL EN 2 VARIABLES",
            "",
            f"Problema: {problem.name}",
            "",
            "VARIABLES DE DECISION:",
            "   x, y >= 0",
            "",
            "FUNCION OBJETIVO:",
            f"   {verbo}  Z = {self._fmt_coef(objective.c1, 'x', first=True)} {self._fmt_coef(objective.c2, 'y')}",
            f"   donde  c1 = {objective.c1:g}   c2 = {objective.c2:g}",
            "",
            "RESTRICCIONES:",
        ]
        for i, c in enumerate(problem.constraints, start=1):
            lines.append(f"   R{i}:  {c.as_pretty_string()}")
        lines.append("   No-negatividad:  x >= 0,  y >= 0   (automatica)")
        return ExplanationStep(title="1. Planteamiento del modelo", content="\n".join(lines))

    # -----------------------------------------------------------------
    # Paso 2: por que funciona el metodo grafico
    # -----------------------------------------------------------------
    def _step_estrategia(self, problem: LPProblem) -> ExplanationStep:
        verbo_obj = "maximo" if problem.objective.optimization_type is OptimizationType.MAX else "minimo"
        lines = [
            "TEOREMA FUNDAMENTAL DE LA PROGRAMACION LINEAL",
            "",
            "  'Si existe un optimo finito para un problema de PL,",
            "   entonces se encuentra en al menos un VERTICE de la",
            "   region factible.'",
            "",
            "Esto justifica el METODO GRAFICO:",
            "",
            "   1) Encontrar todas las intersecciones de pares de",
            "      restricciones (candidatos a vertice).",
            "",
            "   2) Filtrar solo los puntos FACTIBLES (que cumplen",
            "      TODAS las restricciones simultaneamente).",
            "",
            "   3) Evaluar Z en cada vertice factible.",
            "",
            f"   4) Elegir el vertice con el {verbo_obj} valor de Z.",
        ]
        return ExplanationStep(title="2. Estrategia del metodo grafico", content="\n".join(lines))

    # -----------------------------------------------------------------
    # Paso 3: calculo de intersecciones (sistema 2x2)
    # -----------------------------------------------------------------
    def _step_intersecciones(self, problem: LPProblem) -> ExplanationStep:
        n = len(problem.all_constraints)
        pares = comb(n, 2)
        lines = [
            "CALCULO DE INTERSECCIONES (SISTEMA 2x2)",
            "",
            "Para cada par de restricciones (Ri, Rj) resolvemos:",
            "",
            "     a1_i * x  +  a2_i * y  =  b_i",
            "     a1_j * x  +  a2_j * y  =  b_j",
            "",
            "En forma matricial:",
            "",
            "     [ a1_i  a2_i ] [ x ]   [ b_i ]",
            "     [             ] [   ] = [     ]",
            "     [ a1_j  a2_j ] [ y ]   [ b_j ]",
            "",
            "Calculamos el determinante:",
            "",
            "     det = a1_i * a2_j  -  a1_j * a2_i",
            "",
            "  Si det = 0  -> rectas paralelas  -> sin interseccion.",
            "  Si det != 0 -> punto unico de interseccion (regla de Cramer).",
            "",
            "EN ESTE PROBLEMA:",
            f"   Restricciones (incluyendo x>=0 y y>=0): {n}",
            f"   Pares a evaluar: C({n},2) = {pares}",
        ]
        return ExplanationStep(title="3. Intersecciones de restricciones", content="\n".join(lines))

    # -----------------------------------------------------------------
    # Paso 4: filtrado de factibilidad
    # -----------------------------------------------------------------
    def _step_filtrado(self, problem: LPProblem, solution: LPSolution) -> ExplanationStep:
        vertices = solution.all_vertices
        lines = [
            "FILTRADO DE FACTIBILIDAD",
            "",
            "Un punto (x, y) es FACTIBLE si cumple TODAS las",
            "restricciones simultaneamente. Para cada candidato:",
            "",
            "   Para toda restriccion 'a1*x + a2*y <= b':",
            "      verificar  a1*x + a2*y <= b   ?",
            "",
            "   Para toda restriccion 'a1*x + a2*y >= b':",
            "      verificar  a1*x + a2*y >= b   ?",
            "",
            "   x >= 0 ?    y >= 0 ?",
            "",
            "Si cumple TODAS -> es un vertice factible.",
            "",
            f"VERTICES FACTIBLES ENCONTRADOS: {len(vertices)}",
            "",
        ]
        for v in vertices:
            lines.append(f"   ({v.x:g}, {v.y:g})")
        return ExplanationStep(title="4. Filtrado de vertices factibles", content="\n".join(lines))

    # -----------------------------------------------------------------
    # Paso 5: evaluacion de Z en cada vertice
    # -----------------------------------------------------------------
    def _step_evaluacion(self, problem: LPProblem, solution: LPSolution) -> ExplanationStep:
        obj = problem.objective
        is_max = obj.optimization_type is OptimizationType.MAX
        best_z = solution.optimal_z

        lines = [
            "EVALUACION DE LA FUNCION OBJETIVO",
            "",
            f"   Z = {obj.c1:g}*x + {obj.c2:g}*y",
            "",
            "Evaluamos Z en cada vertice factible:",
            "",
            "   Vertice (x, y)    Calculo                   Z",
            "   " + "-" * 55,
        ]
        for v in solution.all_vertices:
            calc = f"{obj.c1:g}*{v.x:g} + {obj.c2:g}*{v.y:g}"
            marker = ""
            if best_z is not None and abs(v.z_value - best_z) <= 1e-7:
                marker = "  <- " + ("MAX" if is_max else "MIN")
            lines.append(
                f"   ({v.x:g}, {v.y:g})".ljust(20)
                + f"{calc}".ljust(28)
                + f"{v.z_value:g}{marker}"
            )
        return ExplanationStep(title="5. Evaluacion de Z en cada vertice", content="\n".join(lines))

    # -----------------------------------------------------------------
    # Paso 6: seleccion del optimo
    # -----------------------------------------------------------------
    def _step_seleccion(self, problem: LPProblem, solution: LPSolution) -> ExplanationStep:
        is_max = problem.objective.optimization_type is OptimizationType.MAX
        verbo = "MAXIMIZAR" if is_max else "MINIMIZAR"
        adjetivo = "MAYOR" if is_max else "MENOR"
        opt = solution.optimal_vertex
        lines = [
            "SELECCION DEL OPTIMO",
            "",
            f"Como buscamos {verbo}, elegimos el vertice con el",
            f"{adjetivo} valor de Z entre los vertices factibles.",
            "",
            "RESULTADO:",
            "",
            f"   Punto optimo:   (x*, y*) = ({opt.x:g}, {opt.y:g})",
            f"   Valor optimo:   Z*       = {solution.optimal_z:g}",
            "",
        ]
        if solution.alternative_optima:
            lines.append("NOTA: el problema tiene MULTIPLES SOLUCIONES OPTIMAS.")
            lines.append("Otros vertices con el mismo Z*:")
            for v in solution.alternative_optima:
                lines.append(f"   ({v.x:g}, {v.y:g})")
            lines.append("")
            lines.append("Cualquier punto del segmento entre estos vertices")
            lines.append("tambien es optimo.")
        else:
            lines.append("INTERPRETACION:")
            lines.append(f"   Asignar x = {opt.x:g} e y = {opt.y:g} consigue el")
            verb_inter = "mayor" if is_max else "menor"
            lines.append(f"   {verb_inter} valor posible de la funcion objetivo,")
            lines.append(f"   respetando todas las restricciones.")
        return ExplanationStep(title="6. Seleccion del optimo", content="\n".join(lines))

    # -----------------------------------------------------------------
    # Paso 7: restricciones activas y holguras
    # -----------------------------------------------------------------
    def _step_restricciones_activas(
        self, problem: LPProblem, solution: LPSolution
    ) -> ExplanationStep:
        opt = solution.optimal_vertex
        lines = [
            "RESTRICCIONES ACTIVAS Y HOLGURAS",
            "",
            "En el optimo, una restriccion es ACTIVA si se cumple",
            "con IGUALDAD (a1*x + a2*y = b). Si hay diferencia,",
            "esa diferencia se llama HOLGURA (recurso sobrante).",
            "",
            f"En el optimo ({opt.x:g}, {opt.y:g}):",
            "",
        ]
        for i, c in enumerate(problem.constraints, start=1):
            lhs = c.lhs_value(opt.x, opt.y)
            activa = c.is_active_at(opt.x, opt.y)
            tag = "ACTIVA" if activa else "HOLGURA"
            holgura = ""
            if not activa:
                if c.operator is Operator.LE:
                    holgura = f"  (holgura = {c.b - lhs:g})"
                elif c.operator is Operator.GE:
                    holgura = f"  (holgura = {lhs - c.b:g})"
            lines.append(f"   R{i}: {c.as_pretty_string()}")
            lines.append(f"        {lhs:g} {c.operator.value} {c.b:g}   ->  {tag}{holgura}")
        lines.append("")
        lines.append("INTERPRETACION:")
        lines.append("  Las restricciones ACTIVAS son los 'cuellos de botella'.")
        lines.append("  Si se relajan (subir b en <=, bajar b en >=), el optimo")
        lines.append("  podria mejorar. Las restricciones con HOLGURA tienen")
        lines.append("  recurso sin usar al nivel del optimo.")
        return ExplanationStep(
            title="7. Restricciones activas e interpretacion", content="\n".join(lines)
        )

    # -----------------------------------------------------------------
    # Casos especiales
    # -----------------------------------------------------------------
    def _step_infactible(self, problem: LPProblem) -> ExplanationStep:
        lines = [
            "PROBLEMA INFACTIBLE",
            "",
            "Despues de calcular todas las intersecciones,",
            "NINGUN punto cumple simultaneamente todas las",
            "restricciones.",
            "",
            "La REGION FACTIBLE es VACIA.",
            "",
            "Esto significa que las restricciones se contradicen",
            "entre si. Por ejemplo:",
            "",
            "   x + y <= 2",
            "   x + y >= 5",
            "",
            "No existe ningun par (x, y) que cumpla ambas.",
            "",
            "CONCLUSION:",
            "   El problema no tiene solucion. Hay que revisar",
            "   las restricciones (datos, signos o el modelo)",
            "   antes de continuar.",
        ]
        return ExplanationStep(title="4. Conclusion: problema infactible", content="\n".join(lines))

    def _step_no_acotado(self, problem: LPProblem) -> ExplanationStep:
        is_max = problem.objective.optimization_type is OptimizationType.MAX
        direccion = "crecer" if is_max else "decrecer"
        lines = [
            "PROBLEMA NO ACOTADO",
            "",
            "Existen vertices factibles, pero la region factible",
            "no esta cerrada en la direccion en la que Z mejora.",
            "",
            f"La funcion objetivo Z puede {direccion} indefinidamente",
            "sin violar ninguna restriccion.",
            "",
            "Esto suele indicar un error en el modelo:",
            "   - Falta una restriccion de cota superior.",
            "   - Algun signo invertido en las restricciones.",
            "   - El sentido de optimizacion (max/min) es el equivocado.",
            "",
            "CONCLUSION:",
            "   El problema no tiene un optimo finito. Hay que",
            "   revisar el modelo antes de obtener una respuesta.",
        ]
        return ExplanationStep(title="6. Conclusion: problema no acotado", content="\n".join(lines))

    # -----------------------------------------------------------------
    # helpers
    # -----------------------------------------------------------------
    @staticmethod
    def _fmt_coef(coef: float, var: str, first: bool = False) -> str:
        if coef == 0:
            return "" if not first else f"0{var}"
        if first:
            if coef == 1:
                return f"{var}"
            if coef == -1:
                return f"-{var}"
            return f"{coef:g}{var}"
        sign = "+" if coef > 0 else "-"
        magnitude = abs(coef)
        if magnitude == 1:
            return f"{sign} {var}"
        return f"{sign} {magnitude:g}{var}"
