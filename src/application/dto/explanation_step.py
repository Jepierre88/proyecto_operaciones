"""Paso de la explicacion paso a paso del metodo grafico."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExplanationStep:
    title: str
    content: str  # texto multilinea, se renderiza en fuente monoespaciada
