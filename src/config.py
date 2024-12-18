from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    debug: bool = False
    app_port: int = 8000

    class Config:
        env_file = "../.env"

settings = Settings()

