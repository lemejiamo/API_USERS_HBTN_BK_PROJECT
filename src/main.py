import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk import set_tag
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

import controllers.actions.general as general
import controllers.actions.hirings as actions_hirings
import controllers.actions.stand_by as actions_stand_by
import controllers.request.hirings as request_hirings
import controllers.request.stand_by as request_stand_by
import controllers.request.withdrawals as request_withdrawals
from controllers import hunty_section
from settings import Settings

settings = Settings()

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    integrations=[
        StarletteIntegration(transaction_style="endpoint"),
        FastApiIntegration(transaction_style="endpoint"),
    ],
    traces_sample_rate=settings.TRACE_RATE,
)

set_tag("scope", settings.SCOPE)

app = FastAPI(
    title="Mentors API",
    description="API to retrieve information to the mentors",
    version="1.1.1",
    root_path=settings.ROOT_PATH,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOW_METHODS,
    allow_headers=settings.ALLOW_HEADERS,
)

app.include_router(hunty_section.router)
app.include_router(general.router)
app.include_router(actions_hirings.router)
app.include_router(actions_stand_by.router)
app.include_router(request_stand_by.router)
app.include_router(request_withdrawals.router)
app.include_router(request_hirings.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
