"""CLI pipeline for FEMRES parsing, feature generation, and life prediction."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch

from .features import aggregate_features
from .model import BasquinLifeModel
from .parser import parse_femres


def _round_float(value: float, digits: int = 6) -> float:
    return round(float(value), digits)


def _write_json(path: Path, payload: dict[str, float]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _render_report(
    input_path: Path, features: dict[str, float], prediction: dict[str, float]
) -> str:
    return (
        "\n".join(
            [
                "# FEM Pipeline Report",
                "",
                "## Input",
                f"- File: `{input_path}`",
                "",
                "## Features",
                f"- n_nodes: {int(features['n_nodes'])}",
                f"- n_elements: {int(features['n_elements'])}",
                f"- sigma_vm_max: {features['sigma_vm_max']:.6f}",
                f"- sigma_vm_mean: {features['sigma_vm_mean']:.6f}",
                f"- sigma_vm_p95: {features['sigma_vm_p95']:.6f}",
                "",
                "## Prediction",
                f"- log10_life: {prediction['log10_life']:.6f}",
                f"- life_cycles: {prediction['life_cycles']:.6f}",
                "",
                "## Data quality",
                "- Required sections validated: META, NODES, ELEMENTS, STEP, STRESS",
                "- Connectivity checks passed: element->node references",
                "- Stress checks passed: stress->element references",
            ]
        )
        + "\n"
    )


def run_pipeline(input_path: Path, outdir: Path) -> dict[str, Path]:
    record = parse_femres(input_path)
    features = aggregate_features(record)

    sigma = torch.tensor([features["sigma_vm_max"]], dtype=torch.float32)
    model = BasquinLifeModel()
    log10_life = model.predict_log10_life(sigma)[0].item()
    life_cycles = model(sigma)[0].item()

    rounded_features = {k: _round_float(v) for k, v in features.items()}
    prediction = {
        "sigma_vm_max": _round_float(features["sigma_vm_max"]),
        "log10_life": _round_float(log10_life),
        "life_cycles": _round_float(life_cycles),
    }

    outdir.mkdir(parents=True, exist_ok=True)
    features_path = outdir / "features.json"
    prediction_path = outdir / "prediction.json"
    report_path = outdir / "report.md"

    _write_json(features_path, rounded_features)
    _write_json(prediction_path, prediction)
    report_path.write_text(
        _render_report(input_path, rounded_features, prediction), encoding="utf-8"
    )

    return {
        "features": features_path,
        "prediction": prediction_path,
        "report": report_path,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run FEM pipeline and write deterministic artifacts"
    )
    parser.add_argument("--input", required=True, type=Path, help="Path to FEMRES input file")
    parser.add_argument("--outdir", required=True, type=Path, help="Directory for output artifacts")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    outputs = run_pipeline(args.input, args.outdir)
    for name in ("features", "prediction", "report"):
        print(f"{name}: {outputs[name]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
