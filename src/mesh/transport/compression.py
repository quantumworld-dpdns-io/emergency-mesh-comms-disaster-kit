from __future__ import annotations

import zstandard as zstd


class CompressionCodec:
    def __init__(self) -> None:
        self._compressor = zstd.ZstdCompressor()
        self._decompressor = zstd.ZstdDecompressor()

    def compress(self, payload: bytes) -> bytes:
        return self._compressor.compress(payload)

    def decompress(self, payload: bytes) -> bytes:
        return self._decompressor.decompress(payload)
