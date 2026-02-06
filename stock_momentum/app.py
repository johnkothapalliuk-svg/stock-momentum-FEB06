from __future__ import annotations

import json
import logging
from dataclasses import asdict

from stock_momentum.adapters.zerodha_adapter import ZerodhaKiteClient
from stock_momentum.config import load_config
from stock_momentum.orchestrator.execution_orchestrator import ExecutionOrchestrator
from stock_momentum.services.market_data_service import MarketDataService
from stock_momentum.services.signal_service import SignalService


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    config = load_config()

    if not config.zerodha.api_key or not config.zerodha.access_token:
        raise RuntimeError(
            "Missing Zerodha credentials. Set ZERODHA_API_KEY and ZERODHA_ACCESS_TOKEN."
        )

    client = ZerodhaKiteClient(
        api_key=config.zerodha.api_key,
        access_token=config.zerodha.access_token,
    )
    market_data_service = MarketDataService(client=client)
    signal_service = SignalService(
        volume_window=config.momentum.volume_window,
        volume_ratio_threshold=config.momentum.volume_ratio_threshold,
    )
    orchestrator = ExecutionOrchestrator(
        market_data_service=market_data_service,
        signal_service=signal_service,
    )

    events = orchestrator.generate_signals(config.instruments)
    signals = orchestrator.summarize(events)
    output = [asdict(signal) for signal in signals]
    print(json.dumps(output, default=str, indent=2))


if __name__ == "__main__":
    main()
