from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import logging

from stock_momentum.domain.events import SignalGenerated
from stock_momentum.domain.models import MomentumSignal
from stock_momentum.services.market_data_service import MarketDataService
from stock_momentum.services.signal_service import SignalService

logger = logging.getLogger(__name__)


@dataclass
class ExecutionOrchestrator:
    market_data_service: MarketDataService
    signal_service: SignalService

    def generate_signals(self, symbols: list[str]) -> list[SignalGenerated]:
        events: list[SignalGenerated] = []
        for symbol in symbols:
            candles = self.market_data_service.get_recent_daily_candles(
                symbol, window=self.signal_service.volume_window
            )
            signal = self.signal_service.compute_signal(symbol, candles)
            events.append(SignalGenerated(created_at=datetime.utcnow(), signal=signal))
            logger.info("Signal generated", extra={"symbol": symbol, "signal": signal})
        return events

    def summarize(self, events: list[SignalGenerated]) -> list[MomentumSignal]:
        return [event.signal for event in events]
