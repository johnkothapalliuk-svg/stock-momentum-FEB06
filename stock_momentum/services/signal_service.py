from __future__ import annotations

from dataclasses import dataclass
from statistics import mean

from stock_momentum.domain.models import Candle, MomentumSignal


@dataclass
class SignalService:
    volume_window: int
    volume_ratio_threshold: float

    def compute_signal(self, symbol: str, candles: list[Candle]) -> MomentumSignal:
        if len(candles) < self.volume_window:
            raise ValueError(
                f"Need at least {self.volume_window} candles to compute momentum."
            )
        recent = candles[-self.volume_window :]
        average_volume = mean(candle.volume for candle in recent)
        latest = recent[-1]
        volume_ratio = latest.volume / average_volume if average_volume else 0.0
        is_momentum = volume_ratio >= self.volume_ratio_threshold
        return MomentumSignal(
            symbol=symbol,
            trading_day=latest.trading_day,
            latest_volume=latest.volume,
            average_volume=average_volume,
            volume_ratio=volume_ratio,
            is_momentum=is_momentum,
        )
