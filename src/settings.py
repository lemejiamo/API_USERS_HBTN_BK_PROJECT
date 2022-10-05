import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    PORT = int(os.getenv("PORT", 8000))
    MACHINE = os.getenv("MACHINE")

    if MACHINE == "GCP":
        ROOT_PATH = "/mentor"
    else:
        ROOT_PATH = ""

    BASE_URL = os.getenv("BASE_URL")
    USERS_RAW_URL = os.getenv("USERS_RAW_URL")
    VACANCY_RAW_URL = os.getenv("VACANCY_RAW_URL")

    USERS_ROOT_PATH = "/user"
    JOB_ROOT_PATH = "/job"
    VACANCY_ROOT_PATH = "/vacancy"

    USER_API_URL = os.getenv("USER_API_URL")
    JOB_API_URL = os.getenv("JOB_API_URL")
    VACANCY_API_URL = os.getenv("VACANCY_API_URL")

    if not USER_API_URL:
        USER_API_URL = f"{BASE_URL}{USERS_ROOT_PATH}"
    if not JOB_API_URL:
        JOB_API_URL = f"{BASE_URL}{JOB_ROOT_PATH}"
    if not VACANCY_API_URL:
        VACANCY_API_URL = f"{BASE_URL}{VACANCY_ROOT_PATH}"

    ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS")
    ALLOW_CREDENTIALS = os.getenv("ALLOW_CREDENTIALS")
    ALLOW_METHODS = os.getenv("ALLOW_METHODS")
    ALLOW_HEADERS = os.getenv("ALLOW_HEADERS")

    LOGIN = False if os.getenv("LOGIN") == "False" else True

    BUCKET_OFFER = os.getenv("BUCKET_OFFER")

    SCOPE = os.getenv("SCOPE")
    TRACE_RATE = os.getenv("TRACE_RATE")
    SENTRY_DSN = os.getenv("SENTRY_DSN")
