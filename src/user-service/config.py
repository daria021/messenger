from pydantic import SecretStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    SECRET: str
    JWT_SECRET: SecretStr
    ACCESS_EXPIRE_DAYS: int
    REFRESH_EXPIRE_DAYS: int

    @property
    def db_user_uri(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()
