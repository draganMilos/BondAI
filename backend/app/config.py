import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = os.getenv("ENV", "dev")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db:5432/copilot")
    # Safety thresholds
    MAX_MSG_LEN: int = 1000
    TOXICITY_BLOCK: float = 0.85
    SEXUALITY_SENSITIVITY: float = 0.80
    LOG_PROMPTS: bool = True
    DISCLOSURE_DEFAULT: bool = False  # user‑toggled in persona

settings = Settings()
