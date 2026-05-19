from __future__ import annotations

import wasmtime


def build_minimal_wasi() -> wasmtime.WasiConfig:
    cfg = wasmtime.WasiConfig()
    cfg.inherit_stdout()
    cfg.inherit_stderr()
    # Intentionally avoid granting filesystem or network capabilities.
    return cfg
