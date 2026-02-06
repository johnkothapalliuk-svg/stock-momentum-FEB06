# Stock Momentum (Zerodha Kite)

This project computes daily stock momentum based on volume using Zerodha Kite historical data. The layout follows the event-driven architecture from the provided diagrams: adapters fetch market data, the signal service generates `SIGNAL_GENERATED` events, and the orchestrator fans them out for downstream execution decisions.

## Architecture Mapping

- **Adapters**: `stock_momentum/adapters/zerodha_adapter.py` provides a Zerodha Kite client.
- **Signal Generation**: `stock_momentum/services/signal_service.py` computes volume-based momentum signals.
- **Orchestrator**: `stock_momentum/orchestrator/execution_orchestrator.py` generates and collects `SIGNAL_GENERATED` events.

## Install

```bash
pip install kiteconnect
```

## Configure

Set environment variables:

```bash
export ZERODHA_API_KEY="your_key"
export ZERODHA_ACCESS_TOKEN="your_access_token"
export INSTRUMENTS="RELIANCE,INFY,TCS"
export VOLUME_WINDOW=20
export VOLUME_RATIO_THRESHOLD=1.5
```

## Run

```bash
python -m stock_momentum.app
```

The output prints JSON with the latest volume, average volume, ratio, and the momentum flag per symbol.
