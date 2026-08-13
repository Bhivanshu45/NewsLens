from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str

    database_url: str
    redis_url: str
    # upstash_redis_rest_url: str
    # upstash_redis_rest_token: str
    qdrant_url: str
    qdrant_api_key: str

    groq_api_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()