from __future__ import annotations

from dataclasses import dataclass

import wasmtime

from .engine import WasmEngine
from .wasi_config import build_minimal_wasi


@dataclass(slots=True)
class LoaderConfig:
    fuel_limit: int = 1_000_000


class WasmPluginLoader:
    def __init__(self, config: LoaderConfig | None = None) -> None:
        self.config = config or LoaderConfig()
        self._engine = WasmEngine.instance()

    def instantiate(self, wasm_path: str) -> tuple[wasmtime.Store, wasmtime.Instance]:
        module = self._engine.get_module(wasm_path)
        linker = wasmtime.Linker(self._engine.engine)

        store = wasmtime.Store(self._engine.engine)
        store.set_fuel(self.config.fuel_limit)
        store.set_wasi(build_minimal_wasi())
        linker.define_wasi()

        instance = linker.instantiate(store, module)
        return store, instance
