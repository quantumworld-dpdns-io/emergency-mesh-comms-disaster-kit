from src.ai.models.ollama_client import OllamaClient


def test_ollama_client_constructs() -> None:
    c = OllamaClient("http://localhost:11434")
    assert c.base_url == "http://localhost:11434"
