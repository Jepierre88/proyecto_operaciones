from __future__ import annotations

from pathlib import Path

import pytest

from src.infrastructure.persistence.xlsx_problem_loader import XlsxProblemLoader


@pytest.fixture
def loader() -> XlsxProblemLoader:
    return XlsxProblemLoader()


def test_supports_xlsx_only(loader, tmp_path):
    assert loader.supports(tmp_path / "x.xlsx")
    assert not loader.supports(tmp_path / "x.json")
    assert not loader.supports(tmp_path / "x.csv")


def test_template_with_example_round_trips(loader, tmp_path):
    template_path = tmp_path / "plantilla.xlsx"
    loader.save_template(template_path, with_example=True)
    assert template_path.exists()
    assert template_path.stat().st_size > 0

    request = loader.load(template_path)
    assert request.objective_type == "max"
    assert request.c1 == 3
    assert request.c2 == 5
    assert len(request.constraints) == 3
    assert request.constraints[0].a1 == 1
    assert request.constraints[0].operator == "<="
    assert request.constraints[2].b == 18


def test_template_empty_has_no_constraints(loader, tmp_path):
    template_path = tmp_path / "vacia.xlsx"
    loader.save_template(template_path, with_example=False)
    request = loader.load(template_path)
    assert request.constraints == []


def test_load_stops_at_first_empty_row(loader, tmp_path):
    """La lectura debe detenerse en la primera fila completamente vacia."""
    from openpyxl import load_workbook

    template_path = tmp_path / "con_hueco.xlsx"
    loader.save_template(template_path, with_example=True)

    wb = load_workbook(template_path)
    sheet = wb["Problema"]
    sheet["A8"] = None
    sheet["B8"] = None
    sheet["C8"] = None
    sheet["D8"] = None
    sheet["E8"] = None
    sheet["A9"] = 99
    sheet["B9"] = 99
    sheet["C9"] = "<="
    sheet["D9"] = 99
    wb.save(template_path)

    request = loader.load(template_path)
    assert len(request.constraints) == 1
    assert request.constraints[0].a1 == 1
