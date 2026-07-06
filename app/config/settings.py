"""
Application Settings
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    APP_NAME = os.getenv(
        "APP_NAME",
        "Learning Roadmap Concierge AI"
    )

    MODEL_NAME = os.getenv(
        "MODEL_NAME",
        "gemini-2.5-flash"
    )

    GOOGLE_API_KEY = os.getenv(
        "GOOGLE_API_KEY"
    )

    DEBUG = os.getenv(
        "DEBUG",
        "True"
    )


settings = Settings()
