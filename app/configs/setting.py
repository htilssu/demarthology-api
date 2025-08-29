from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017"
    
    # Cloudinary configuration
    CLOUDINARY_URL: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


setting = Setting()
