from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://admin:securepassword123@localhost:5432/logistics"
    SECRET_KEY: str = "super_secret_jwt_key_change_in_prod"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()