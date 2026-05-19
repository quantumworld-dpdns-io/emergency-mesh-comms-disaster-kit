from __future__ import annotations

from pathlib import Path

import wasmtime


class WasmEngine:
    _instance: "WasmEngine | None" = None

    def __init__(self) -> None:
        config = wasmtime.Config()
        config.wasm_simd = True
        config.consume_fuel = True
        config.epoch_interruption = True
        self.engine = wasmtime.Engine(config)
        self._module_cache: dict[str, wasmtime.Module] = {}

    @classmethod
    def instance(cls) -> "WasmEngine":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_module(self, wasm_path: str) -> wasmtime.Module:
        p = str(Path(wasm_path).resolve())
        if p not in self._module_cache:
            self._module_cache[p] = wasmtime.Module.from_file(self.engine, p)
        return self._module_cache[p]
