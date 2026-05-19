from __future__ import annotations

from pathlib import Path


class WasmTransportPluginLoader:
    def __init__(self, plugin_dir: str) -> None:
        self.plugin_dir = Path(plugin_dir)

    def discover_plugins(self) -> list[Path]:
        if not self.plugin_dir.exists():
            return []
        return sorted(self.plugin_dir.glob("*.wasm"))
