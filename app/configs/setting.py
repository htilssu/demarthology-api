from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    MONGO_URI: str = 'mongodb://localhost:27017'
    JWT_SECRET: str = 'your-secret-key-change-this-in-production'
    JWT_ALGORITHM: str = 'HS256'
    JWT_EXPIRATION_HOURS: int = 24

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


setting = Setting()
