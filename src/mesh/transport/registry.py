from __future__ import annotations

from .base import Transport


class TransportRegistry:
    def __init__(self) -> None:
        self._transports: dict[str, Transport] = {}

    def register(self, transport: Transport) -> None:
        self._transports[transport.name] = transport

    def unregister(self, name: str) -> None:
        self._transports.pop(name, None)

    def get(self, name: str) -> Transport | None:
        return self._transports.get(name)

    def list_names(self) -> list[str]:
        return list(self._transports.keys())

    @property
    def transports(self) -> dict[str, Transport]:
        return dict(self._transports)
