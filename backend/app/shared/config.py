from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration. Reads from environment, then `.env`."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = Field(..., alias="DATABASE_URL")
    redis_url: str = Field(..., alias="REDIS_URL")
    jwt_secret: str = Field(..., alias="JWT_SECRET")
    jwt_alg: str = Field("HS256", alias="JWT_ALG")
    jwt_ttl_min: int = Field(10080, alias="JWT_TTL_MIN")
    cors_origins: str = Field("http://localhost:3000", alias="CORS_ORIGINS")

    media_storage_backend: str = Field("local", alias="MEDIA_STORAGE_BACKEND")
    media_root: str = Field("./media", alias="MEDIA_ROOT")
    minio_bucket: str | None = Field(None, alias="MINIO_BUCKET")
    minio_region: str | None = Field(None, alias="MINIO_REGION")
    minio_endpoint_url: str | None = Field(None, alias="MINIO_ENDPOINT_URL")
    minio_access_key: str | None = Field(None, alias="MINIO_ACCESS_KEY")
    minio_secret_key: str | None = Field(None, alias="MINIO_SECRET_KEY")
    minio_signed_url_ttl_seconds: int = Field(3600, alias="MINIO_SIGNED_URL_TTL_SECONDS")

    gemini_api_key: str | None = Field(None, alias="GEMINI_API_KEY")
    gemini_api_base_url: str = Field(
        "https://generativelanguage.googleapis.com/v1beta", alias="GEMINI_API_BASE_URL"
    )
    content_gen_model: str = Field("gemini-2.5-flash", alias="CONTENT_GEN_MODEL")


def get_settings() -> Settings:
    return Settings()
