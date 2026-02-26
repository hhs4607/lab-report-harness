"""Basquin-like PyTorch model for fatigue-life prediction."""

from __future__ import annotations

import torch
from torch import nn


class BasquinLifeModel(nn.Module):
    """Predict fatigue life from stress using log10(N) = A - B*log10(sigma).

    Constants are fixed for deterministic behavior in this harness:
    - A = 12.0
    - B = 3.0
    """

    def __init__(self, a: float = 12.0, b: float = 3.0) -> None:
        super().__init__()
        self.register_buffer("a", torch.tensor(float(a), dtype=torch.float32))
        self.register_buffer("b", torch.tensor(float(b), dtype=torch.float32))

    def predict_log10_life(self, sigma_vm_max: torch.Tensor) -> torch.Tensor:
        sigma_safe = torch.clamp(sigma_vm_max, min=1e-12)
        return self.a - self.b * torch.log10(sigma_safe)

    def forward(self, sigma_vm_max: torch.Tensor) -> torch.Tensor:
        log10_life = self.predict_log10_life(sigma_vm_max)
        base = torch.tensor(10.0, dtype=log10_life.dtype, device=log10_life.device)
        return torch.pow(base, log10_life)
