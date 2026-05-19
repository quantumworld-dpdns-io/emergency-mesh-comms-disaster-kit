from src.lora.packets.arq import StopAndWaitArq


def test_arq_ack_flow() -> None:
    arq = StopAndWaitArq()
    arq.begin_send(7)
    assert arq.on_ack(7)
    assert not arq.on_ack(7)
