from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str
    openai_api_base: str
    openai_model: str
    db_name: str
    db_user: str
    db_password: str
    db_host: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
