"""Caso de uso: cargar un ProblemRequest desde archivo (JSON o CSV)."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from src.application.dto.problem_request import ProblemRequest


class ProblemLoader(Protocol):
    def load(self, path: Path) -> ProblemRequest: ...
    def supports(self, path: Path) -> bool: ...


class LoadProblemFromFileUseCase:
    def __init__(self, loaders: list[ProblemLoader]) -> None:
        self._loaders = loaders

    def execute(self, path: str | Path) -> ProblemRequest:
        target = Path(path)
        if not target.exists():
            raise FileNotFoundError(f"No existe el archivo: {target}")
        for loader in self._loaders:
            if loader.supports(target):
                return loader.load(target)
        raise ValueError(f"Formato no soportado: {target.suffix}")
