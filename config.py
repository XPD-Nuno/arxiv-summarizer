"""
Configuration management for arXiv summarizer.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration."""

    # Environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

    # arXiv API
    ARXIV_BASE_URL = os.getenv("ARXIV_BASE_URL")

    # Request config
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
    MAX_RESULTS = int(os.getenv("MAX_RESULTS", "5"))
    REQUEST_DELAY = int(os.getenv("REQUEST_DELAY", "3"))

    @classmethod
    def validate(cls):
        """Validate required config."""
        if not cls.ARXIV_BASE_URL:
            raise ValueError("Missing ARXIV_BASE_URL in .env")

        print(f"✅ Config validated for {cls.ENVIRONMENT}")


# Validate on import
Config.validate()


if __name__ == "__main__":
    print("Running config check...")