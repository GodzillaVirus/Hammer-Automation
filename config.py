import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    telegram_bot_token: str = "8563563429:AAGLW_hCpbeC2-JfStd_bveMWiBsaTaOh-E"
    telegram_chat_id: int = 5328767896
    port: int = 8000
    host: str = "0.0.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
