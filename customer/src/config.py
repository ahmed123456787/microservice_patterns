from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    RABBITMQ_BROKER_URL: str = Field(..., env="RABBITMQ_BROKER_URL")
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    DATABASE_NAME: str = Field(..., env="DATABASE_NAME")
    DATABASE_USER: str = Field(..., env="DATABASE_USER")
    DATABASE_PASSWORD: str = Field(..., env="DATABASE_PASSWORD")
    DATABASE_HOST: str = Field(..., env="DATABASE_HOST")
    DATABASE_PORT: int = Field(..., env="DATABASE_PORT")
    RABBITMQ_PORT: int = Field(..., env="RABBITMQ_PORT")
    RABBITMQ_HOST: str = Field(..., env="RABBITMQ_HOST")
    RABBITMQ_USER: str = Field(..., env="RABBITMQ_USER")
    RABBITMQ_PASSWORD: str = Field(..., env="RABBITMQ_PASSWORD")


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()