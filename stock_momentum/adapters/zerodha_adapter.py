from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Iterable, Protocol

try:
    from kiteconnect import KiteConnect
except ImportError:  # pragma: no cover - optional dependency
    KiteConnect = None  # type: ignore[assignment]

from stock_momentum.domain.models import Candle


class MarketDataClient(Protocol):
    def fetch_daily_candles(self, symbol: str, start: date, end: date) -> list[Candle]:
        """Return daily candles for the symbol in the date range."""


@dataclass
class ZerodhaKiteClient:
    api_key: str
    access_token: str

    def __post_init__(self) -> None:
        if KiteConnect is None:
            raise RuntimeError(
                "kiteconnect is not installed. Install it with `pip install kiteconnect`."
            )
        self._kite = KiteConnect(api_key=self.api_key)
        self._kite.set_access_token(self.access_token)

    def fetch_daily_candles(self, symbol: str, start: date, end: date) -> list[Candle]:
        if KiteConnect is None:
            raise RuntimeError("kiteconnect is not available")
        instrument_token = self._kite.ltp(symbol)[symbol]["instrument_token"]
        data = self._kite.historical_data(
            instrument_token=instrument_token,
            from_date=start,
            to_date=end,
            interval="day",
        )
        return [
            Candle(
                trading_day=record["date"].date()
                if isinstance(record["date"], datetime)
                else record["date"],
                open=record["open"],
                high=record["high"],
                low=record["low"],
                close=record["close"],
                volume=int(record["volume"]),
            )
            for record in data
        ]


@dataclass
class InMemoryMarketDataClient:
    """Simple client for tests or dry runs."""

    candles_by_symbol: dict[str, list[Candle]]

    def fetch_daily_candles(self, symbol: str, start: date, end: date) -> list[Candle]:
        candles = self.candles_by_symbol.get(symbol, [])
        return [candle for candle in candles if start <= candle.trading_day <= end]


def ensure_minimum_candles(candles: Iterable[Candle], minimum: int) -> list[Candle]:
    """Ensure there are at least `minimum` candles available."""
    candle_list = list(candles)
    if len(candle_list) < minimum:
        raise ValueError(
            f"Expected at least {minimum} candles, got {len(candle_list)}."
        )
    return candle_list
