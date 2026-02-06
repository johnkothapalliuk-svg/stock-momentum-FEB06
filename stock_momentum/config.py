from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class ZerodhaConfig:
    api_key: str
    access_token: str
    api_secret: str | None = None


@dataclass(frozen=True)
class MomentumConfig:
    volume_window: int
    volume_ratio_threshold: float


@dataclass(frozen=True)
class AppConfig:
    zerodha: ZerodhaConfig
    momentum: MomentumConfig
    instruments: list[str]



def load_config() -> AppConfig:
    """Load configuration from environment variables."""
    instruments = [
        symbol.strip()
        for symbol in os.getenv("INSTRUMENTS", "RELIANCE,NIFTY 50").split(",")
        if symbol.strip()
    ]
    volume_window = int(os.getenv("VOLUME_WINDOW", "20"))
    volume_ratio_threshold = float(os.getenv("VOLUME_RATIO_THRESHOLD", "1.5"))
    api_key = os.getenv("ZERODHA_API_KEY", "")
    access_token = os.getenv("ZERODHA_ACCESS_TOKEN", "")
    api_secret = os.getenv("ZERODHA_API_SECRET")

    return AppConfig(
        zerodha=ZerodhaConfig(
            api_key=api_key,
            access_token=access_token,
            api_secret=api_secret,
        ),
        momentum=MomentumConfig(
            volume_window=volume_window,
            volume_ratio_threshold=volume_ratio_threshold,
        ),
        instruments=instruments,
    )
