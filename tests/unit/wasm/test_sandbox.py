from __future__ import annotations

import pytest

from src.wasm.loader import LoaderConfig, WasmPluginLoader


def test_loader_config_defaults() -> None:
    cfg = LoaderConfig()
    assert cfg.fuel_limit == 1_000_000


@pytest.mark.unit
def test_loader_initializes() -> None:
    loader = WasmPluginLoader()
    assert loader.config.fuel_limit > 0
