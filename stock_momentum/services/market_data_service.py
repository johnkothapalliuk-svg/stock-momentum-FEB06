from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from stock_momentum.adapters.zerodha_adapter import MarketDataClient
from stock_momentum.domain.models import Candle


@dataclass
class MarketDataService:
    client: MarketDataClient

    def get_recent_daily_candles(self, symbol: str, window: int) -> list[Candle]:
        end = date.today()
        start = end - timedelta(days=window * 2)
        candles = self.client.fetch_daily_candles(symbol, start=start, end=end)
        candles_sorted = sorted(candles, key=lambda c: c.trading_day)
        return candles_sorted[-window:]
