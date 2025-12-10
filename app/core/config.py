from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str = "root"
    DB_PASS: str = ""
    DB_HOST: str = "127.0.0.1"
    DB_NAME: str = "fastapi_db"
    
    SECRET_KEY: str = "MASTER_SECRET_KEY"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    class Config:
        env_file = ".env"

settings = Settings()
