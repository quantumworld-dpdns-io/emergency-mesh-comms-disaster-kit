import pytest

from src.mesh.transport.simulated import SimulatedTransport


@pytest.mark.asyncio
async def test_simulated_transport_send_receive() -> None:
    t = SimulatedTransport(loss_rate=0.0, delay_ms=0)
    await t.send("node-2", b"hello")
    src, payload = await t.receive()
    assert src == "node-2"
    assert payload == b"hello"
