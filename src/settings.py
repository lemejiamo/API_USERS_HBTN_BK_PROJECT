import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    PORT = int(os.getenv("PORT", 8000))
    MACHINE = os.getenv("MACHINE")

    if MACHINE == "GCP":
        ROOT_PATH = "/login"
    else:
        ROOT_PATH = ""

    BASE_URL = os.getenv("BASE_URL")
    CRUD_RAW_URL = os.getenv("USERS_RAW_URL")
    PRODUCT_RAW_URL = os.getenv("VACANCY_RAW_URL")

    CRUD_ROOT_PATH = "/crud"
    PRODUCT_ROOT_PATH = "/product"

    CRUD_API_URL = os.getenv("CRUD_API_URL")
    PRODUCT_API_URL = os.getenv("JOB_API_URL")

    if not CRUD_API_URL:
        CRUD_API_URL = f"{BASE_URL}{CRUD_ROOT_PATH}"
    if not PRODUCT_API_URL:
        JOB_API_URL = f"{BASE_URL}{PRODUCT_ROOT_PATH}"

    ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS")
    ALLOW_CREDENTIALS = os.getenv("ALLOW_CREDENTIALS")
    ALLOW_METHODS = os.getenv("ALLOW_METHODS")
    ALLOW_HEADERS = os.getenv("ALLOW_HEADERS")

    SECRET_TOKEN = os.getenv("SECRET_TOKEN")
    TOKEN_ALGORITHM = os.getenv("TOKEN_ALGORITHM")
    LOGIN = False if os.getenv("LOGIN") == "False" else True
