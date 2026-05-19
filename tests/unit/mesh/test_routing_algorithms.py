from src.mesh.router.epidemic import EpidemicRouter
from src.mesh.router.prophet import ProphetRouter
from src.mesh.router.spray_wait import SprayWaitRouter


def test_epidemic_missing_summary() -> None:
    assert EpidemicRouter.missing_bundles({"a", "b"}, {"a"}) == {"b"}


def test_prophet_updates() -> None:
    r = ProphetRouter()
    r.on_encounter("a", "b")
    assert r.predictability[("a", "b")] > 0


def test_spray_wait_tokens() -> None:
    r = SprayWaitRouter(initial_tokens=8)
    r.init_bundle("b1")
    assert r.can_spray("b1")
    assert r.spray("b1") >= 1
