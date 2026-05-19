from __future__ import annotations

from src.mesh.protocol.bundle import Bundle

from ..loader import WasmPluginLoader


class RoutingPluginCaller:
    def __init__(self, wasm_path: str) -> None:
        self.wasm_path = wasm_path
        self.loader = WasmPluginLoader()

    def should_forward(self, bundle: Bundle, lqi: int) -> bool:
        store, instance = self.loader.instantiate(self.wasm_path)
        fn = instance.exports(store).get("should_forward")
        if fn is None:
            return True
        priority = {"general": 1, "medical": 2, "emergency": 3}[bundle.primary.priority.value]
        result = fn(store, priority, lqi)
        return bool(result)
