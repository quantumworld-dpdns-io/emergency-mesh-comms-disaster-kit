from __future__ import annotations

import asyncio
import json
import socket
from dataclasses import dataclass


MULTICAST_GROUP = "224.0.0.251"
MULTICAST_PORT = 4554


@dataclass(slots=True)
class Beacon:
    node_id: str
    eid: str
    lqi: float


class BeaconService:
    async def send_once(self, beacon: Beacon) -> None:
        loop = asyncio.get_running_loop()
        payload = json.dumps(beacon.__dict__).encode("utf-8")

        def _send() -> None:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
            sock.sendto(payload, (MULTICAST_GROUP, MULTICAST_PORT))
            sock.close()

        await loop.run_in_executor(None, _send)
