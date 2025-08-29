from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    MONGO_URI: str = 'mongodb://localhost:27017'
    JWT_SECRET_KEY: str = 'your-secret-key-here-change-in-production'
    JWT_ALGORITHM: str = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


setting = Setting()
