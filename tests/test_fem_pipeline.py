from __future__ import annotations

import json
from pathlib import Path

import pytest
import torch

from lab_report.fem.features import aggregate_features
from lab_report.fem.model import BasquinLifeModel
from lab_report.fem.parser import parse_femres
from lab_report.fem.pipeline import run_pipeline


def _fixture_path(name: str) -> Path:
    return Path("tests/fixtures/fem") / name


def _predict_sigma_vm_max(features: dict[str, float]) -> tuple[float, float]:
    model = BasquinLifeModel()
    sigma = torch.tensor([features["sigma_vm_max"]], dtype=torch.float32)
    log10_life = model.predict_log10_life(sigma)[0].item()
    life_cycles = model(sigma)[0].item()
    return log10_life, life_cycles


def test_parser_errors_include_line_numbers(tmp_path: Path) -> None:
    bad_content = """FEMRES,1.0
META
case_id,bad_case
load_level,low
NODES
id,x,y,z
1,0.0,0.0,0.0
ELEMENTS
id,n1,n2,n3
101,1,1,1
STEP
name,step_1
STRESS
element_id,sxx,syy,szz,sxy,syz,szx
101,abc,85.0,40.0,12.0,4.0,6.0
END
"""
    path = tmp_path / "invalid.femres"
    path.write_text(bad_content, encoding="utf-8")

    with pytest.raises(ValueError) as excinfo:
        parse_femres(path)

    message = str(excinfo.value)
    assert str(path) in message
    assert ":15:" in message
    assert "non-numeric sxx" in message


def test_features_invariant_to_order() -> None:
    low_record = parse_femres(_fixture_path("cantilever_low.femres"))
    shuffled_record = parse_femres(_fixture_path("cantilever_low_shuffled.femres"))

    low_features = aggregate_features(low_record)
    shuffled_features = aggregate_features(shuffled_record)

    assert low_features["n_nodes"] == shuffled_features["n_nodes"]
    assert low_features["n_elements"] == shuffled_features["n_elements"]
    assert low_features["sigma_vm_max"] == pytest.approx(shuffled_features["sigma_vm_max"])
    assert low_features["sigma_vm_mean"] == pytest.approx(shuffled_features["sigma_vm_mean"])
    assert low_features["sigma_vm_p95"] == pytest.approx(shuffled_features["sigma_vm_p95"])

    low_log10, low_life = _predict_sigma_vm_max(low_features)
    shuffled_log10, shuffled_life = _predict_sigma_vm_max(shuffled_features)
    assert low_log10 == pytest.approx(shuffled_log10, rel=1e-8)
    assert low_life == pytest.approx(shuffled_life, rel=1e-8)


def test_monotonic_life_with_stress() -> None:
    low_features = aggregate_features(parse_femres(_fixture_path("cantilever_low.femres")))
    high_features = aggregate_features(parse_femres(_fixture_path("cantilever_high.femres")))

    _, low_life = _predict_sigma_vm_max(low_features)
    _, high_life = _predict_sigma_vm_max(high_features)
    assert high_life < low_life


def test_autograd_gradient_sign() -> None:
    model = BasquinLifeModel()
    sigma = torch.tensor([150.0], dtype=torch.float32, requires_grad=True)
    log10_life = model.predict_log10_life(sigma).sum()
    log10_life.backward()
    assert sigma.grad is not None
    assert sigma.grad.item() < 0.0


def test_pipeline_e2e_golden(tmp_path: Path) -> None:
    outputs = run_pipeline(_fixture_path("cantilever_low.femres"), tmp_path)

    features = json.loads(outputs["features"].read_text(encoding="utf-8"))
    prediction = json.loads(outputs["prediction"].read_text(encoding="utf-8"))
    report = outputs["report"].read_text(encoding="utf-8")

    assert set(features.keys()) == {
        "n_elements",
        "n_nodes",
        "sigma_vm_max",
        "sigma_vm_mean",
        "sigma_vm_p95",
    }

    assert prediction["sigma_vm_max"] == pytest.approx(features["sigma_vm_max"], rel=1e-9)
    expected_log10, expected_life = _predict_sigma_vm_max(features)
    assert prediction["log10_life"] == pytest.approx(round(expected_log10, 6), rel=1e-9)
    assert prediction["life_cycles"] == pytest.approx(round(expected_life, 6), rel=1e-9)

    assert "# FEM Pipeline Report" in report
    assert "## Features" in report
    assert "## Prediction" in report
    assert "## Data quality" in report
