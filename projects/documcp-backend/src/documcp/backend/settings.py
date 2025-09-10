from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from documcp.shared_kernel.domain.enum import ApplicationMode
from documcp.shared_kernel.infra.settings.model import (
    CacheSettings,
    CORSSettings,
    FastAPISettings,
    GZipSettings,
    SessionSettings,
)


class LMStudioSettings(BaseModel):
    """LM Studio configuration."""

    base_url: str = "http://localhost:1234"
    model_name: str = "local-model"
    timeout: float = 300.0


class Settings(BaseSettings):
    """Application settings."""

    mode: ApplicationMode = ApplicationMode.DEVELOPMENT
    cors: CORSSettings = CORSSettings()
    gzip: GZipSettings = GZipSettings()
    cache: CacheSettings = CacheSettings()
    fastapi: FastAPISettings = FastAPISettings(
        title="DocuMCP API",
        description="Document generation API using LM Studio",
        docs_url="/docs",
        openapi_url="/openapi.json",
        redoc_url="/redoc",
    )
    session: SessionSettings = SessionSettings()
    lm_studio: LMStudioSettings = LMStudioSettings()

    model_config = SettingsConfigDict(
        env_prefix="DOCUMCP_", env_nested_delimiter="__", env_file_encoding="utf-8", extra="allow"
    )


Settings.model_rebuild()
