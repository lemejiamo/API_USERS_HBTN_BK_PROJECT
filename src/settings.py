import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    PORT = int(os.getenv("PORT", 8000))

    CRUD_API_URL = os.getenv("CRUD_API_URL")

    ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS")
    ALLOW_CREDENTIALS = os.getenv("ALLOW_CREDENTIALS")
    ALLOW_METHODS = os.getenv("ALLOW_METHODS")
    ALLOW_HEADERS = os.getenv("ALLOW_HEADERS")

    SECRET_TOKEN = os.getenv("SECRET_TOKEN")
    TOKEN_ALGORITHM = os.getenv("TOKEN_ALGORITHM")
