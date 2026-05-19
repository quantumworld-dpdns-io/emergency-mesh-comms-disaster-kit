from __future__ import annotations

from dataclasses import dataclass

from .kdf import hkdf_sha256


@dataclass(slots=True)
class RatchetState:
    root_key: bytes
    send_chain_key: bytes
    recv_chain_key: bytes
    send_count: int = 0
    recv_count: int = 0


class DoubleRatchet:
    def __init__(self, shared_secret: bytes) -> None:
        root = hkdf_sha256(shared_secret, salt=b"dr-root", info=b"root", length=32)
        self.state = RatchetState(root_key=root, send_chain_key=root, recv_chain_key=root)

    def next_send_message_key(self) -> bytes:
        self.state.send_chain_key = hkdf_sha256(
            self.state.send_chain_key,
            salt=self.state.root_key,
            info=f"send-{self.state.send_count}".encode(),
            length=32,
        )
        self.state.send_count += 1
        return self.state.send_chain_key

    def next_recv_message_key(self) -> bytes:
        self.state.recv_chain_key = hkdf_sha256(
            self.state.recv_chain_key,
            salt=self.state.root_key,
            info=f"recv-{self.state.recv_count}".encode(),
            length=32,
        )
        self.state.recv_count += 1
        return self.state.recv_chain_key
