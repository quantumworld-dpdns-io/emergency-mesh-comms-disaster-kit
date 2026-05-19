from __future__ import annotations

import pytest

from src.wasm.engine import WasmEngine


@pytest.mark.integration
def test_wasm_engine_singleton() -> None:
    a = WasmEngine.instance()
    b = WasmEngine.instance()
    assert a is b
