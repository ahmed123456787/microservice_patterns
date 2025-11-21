from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    RABBITMQ_BROKER_URL: str = Field(..., env="RABBITMQ_BROKER_URL")
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    DATABASE_USER: str = Field(..., env="DATABASE_USER")
    DATABASE_PASSWORD: str = Field(..., env="DATABASE_PASSWORD")
    DATABASE_HOST: str = Field(..., env="DATABASE_HOST")    
    DATABASE_PORT: str = Field(..., env="DATABASE_PORT")
    DATABASE_NAME: str = Field(..., env="DATABASE_NAME")
    RABBITMQ_USER: str = Field(..., env="RABBITMQ_USER")
    RABBITMQ_PASSWORD: str = Field(..., env="RABBITMQ_PASSWORD")
    RABBITMQ_HOST: str = Field(..., env="RABBITMQ_HOST")
    RABBITMQ_PORT: str = Field(..., env="RABBITMQ_PORT")
                                   
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()