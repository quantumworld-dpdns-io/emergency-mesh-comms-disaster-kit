from __future__ import annotations

from collections.abc import Callable

from watchfiles import watch


class WasmWatcher:
    def __init__(self, directory: str) -> None:
        self.directory = directory

    def run(self, on_change: Callable[[str], None]) -> None:
        for changes in watch(self.directory):
            for _change, path in changes:
                if path.endswith(".wasm"):
                    on_change(path)
