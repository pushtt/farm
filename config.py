from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    DB_URL: str | None
    DB_NAME: str | None
    CLOUDINARY_SECRET_KEY: str | None
    CLOUDINARY_API_KEY: str | None
    CLOUDINARY_CLOUD_NAME: str | None

    """Loads the dotenv file. Including this is necessary to get
    pydantic to load a .env file."""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
