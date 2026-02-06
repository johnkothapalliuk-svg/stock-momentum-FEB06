from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from stock_momentum.domain.models import MomentumSignal


@dataclass(frozen=True)
class SignalGenerated:
    created_at: datetime
    signal: MomentumSignal
