"""Caso de uso: cargar un problema precargado por nombre."""

from __future__ import annotations

from typing import Protocol

from src.application.dto.problem_request import ProblemRequest


class SampleCatalog(Protocol):
    def list_samples(self) -> list[tuple[str, str]]:
        """Devuelve [(id, display_name), ...]."""

    def get_sample(self, sample_id: str) -> ProblemRequest: ...


class LoadSampleProblemUseCase:
    def __init__(self, catalog: SampleCatalog) -> None:
        self._catalog = catalog

    def list(self) -> list[tuple[str, str]]:
        return self._catalog.list_samples()

    def execute(self, sample_id: str) -> ProblemRequest:
        return self._catalog.get_sample(sample_id)
