from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class GatewayBridge:
    mqtt_broker: str
    topic_prefix: str = "mesh/lora"

    def uplink_topic(self) -> str:
        return f"{self.topic_prefix}/uplink"

    def downlink_topic(self) -> str:
        return f"{self.topic_prefix}/downlink"
