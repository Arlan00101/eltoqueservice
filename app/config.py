import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    ELTOQUE_API_URL = os.getenv("ELTOQUE_API_URL", "https://tasas.eltoque.com/api/v1")
    ELTOQUE_API_KEY = os.getenv("ELTOQUE_API_KEY", "")
    API_KEY = os.getenv("API_KEY", "")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
