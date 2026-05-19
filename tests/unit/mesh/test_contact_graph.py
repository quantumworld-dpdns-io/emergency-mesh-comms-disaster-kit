from src.mesh.router.contact_graph import ContactGraph


def test_shortest_path() -> None:
    g = ContactGraph()
    g.add_edge("a", "b", -50, 20)
    g.add_edge("b", "c", -50, 20)
    assert g.shortest_path("a", "c") == ["a", "b", "c"]
