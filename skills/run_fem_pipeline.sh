#!/usr/bin/env bash
set -euo pipefail

input="tests/fixtures/fem/cantilever_low.femres"
outdir="artifacts/fem_pipeline"

PYTHONPATH="src${PYTHONPATH:+:${PYTHONPATH}}" python -m lab_report.fem.pipeline --input "${input}" --outdir "${outdir}"

echo "outputs:"
echo "- ${outdir}/features.json"
echo "- ${outdir}/prediction.json"
echo "- ${outdir}/report.md"
