from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://admin:securepassword123@127.0.0.1:5433/logistics"
    SECRET_KEY: str = "super_secret_jwt_key_change_in_prod"
    ALGORITHM: str = "HS256"

    MINIO_ENDPOINT: str = "127.0.0.1:9000"
    MINIO_ACCESS_KEY: str = "admin"
    MINIO_SECRET_KEY: str = "securepassword123"
    MINIO_BUCKET_NAME: str = "workshop-submissions"

    class Config:
        env_file = ".env"

settings = Settings()