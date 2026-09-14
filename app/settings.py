from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DB_URL: str
    SECRET_KEY: str
    EXPIRE_IN_MINS: int
    ALGORITHM: str


settings = Settings()  # pyright: ignore[reportCallIssue]
