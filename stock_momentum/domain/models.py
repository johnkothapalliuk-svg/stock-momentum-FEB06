from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Candle:
    trading_day: date
    open: float
    high: float
    low: float
    close: float
    volume: int


@dataclass(frozen=True)
class MomentumSignal:
    symbol: str
    trading_day: date
    latest_volume: int
    average_volume: float
    volume_ratio: float
    is_momentum: bool
