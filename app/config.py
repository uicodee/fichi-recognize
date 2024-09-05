from pydantic_settings import BaseSettings


class Storage(BaseSettings):
    endpoint: str
    region: str
    access_key: str
    secret_key: str
    bucket_id: str


class SettingsExtractor(BaseSettings):
    ENDPOINT: str
    REGION: str
    ACCESS__KEY: str
    SECRET__KEY: str
    BUCKET__ID: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class Settings(BaseSettings):
    storage: Storage


def load_config() -> Settings:
    settings = SettingsExtractor()

    return Settings(
        storage=Storage(
            endpoint=settings.ENDPOINT,
            region=settings.REGION,
            access_key=settings.ACCESS__KEY,
            secret_key=settings.SECRET__KEY,
            bucket_id=settings.BUCKET__ID,
        ),
    )
