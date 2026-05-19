from __future__ import annotations

from ..loader import WasmPluginLoader


class CompressionPluginCaller:
    def __init__(self, wasm_path: str) -> None:
        self.wasm_path = wasm_path
        self.loader = WasmPluginLoader()

    def compress(self, payload: bytes) -> bytes:
        store, instance = self.loader.instantiate(self.wasm_path)
        fn = instance.exports(store).get("compress_stub")
        if fn is not None:
            fn(store)
        return payload

    def decompress(self, payload: bytes) -> bytes:
        store, instance = self.loader.instantiate(self.wasm_path)
        fn = instance.exports(store).get("decompress_stub")
        if fn is not None:
            fn(store)
        return payload
