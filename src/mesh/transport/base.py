from __future__ import annotations

from abc import ABC, abstractmethod


class Transport(ABC):
    name: str

    @abstractmethod
    async def send(self, destination: str, payload: bytes) -> None: ...

    @abstractmethod
    async def receive(self) -> tuple[str, bytes]: ...

    @abstractmethod
    async def discover(self) -> list[str]: ...
