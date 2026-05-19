"""Shared application settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    env: str = "dev"
    log_level: str = "INFO"
    redis_url: str = "redis://localhost:6379/0"
    qdrant_url: str = "http://localhost:6333"
    ollama_url: str = "http://localhost:11434"
    duckdb_path: str = "./data/mesh.duckdb"
    arrow_flight_host: str = "0.0.0.0"
    arrow_flight_port: int = 8815
    lora_enabled: bool = False
    lora_port: str = "/dev/ttyUSB0"
    lora_region: str = "US915"
    secret_key: str = "change-me"


settings = Settings()
