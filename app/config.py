"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All application settings, sourced from .env or environment."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # NVIDIA NIM API
    NVIDIA_API_KEY: str = ""
    NVIDIA_BASE_URL: str = "https://integrate.api.nvidia.com/v1"
    NVIDIA_MODEL: str = "nvidia/llama-3.3-nemotron-super-49b-v1"

    # GitHub App credentials
    GITHUB_APP_ID: str = ""
    GITHUB_PRIVATE_KEY_PATH: str = "./github_private_key.pem"
    GITHUB_PRIVATE_KEY: str = ""  # PEM content as env var (used in cloud deployments)
    GITHUB_WEBHOOK_SECRET: str = ""

    # App settings
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    PORT: int = 8000

    # Feature flags
    FEATURE_TRIAGE: bool = True
    FEATURE_REPRODUCTION: bool = True
    FEATURE_ONBOARDING: bool = True
    FEATURE_PR_REVIEW: bool = True
    FEATURE_RELEASE_NOTES: bool = True


settings = Settings()
