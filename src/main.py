import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html

import controllers.user as user

from settings import Settings

settings = Settings()

app = FastAPI(
    title="Login API",
    description="API to login a user",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOW_METHODS,
    allow_headers=settings.ALLOW_HEADERS,
)

app.include_router(user.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
