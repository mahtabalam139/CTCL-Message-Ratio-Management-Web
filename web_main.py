
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from routes.dashboard import router as dashboard_router
from routes.search import router as search_router

from routes.auth import router as auth_router
from routes import revision
app = FastAPI(
    title="CTCL Message Ratio Management Tool"
)

app.include_router(
    revision.router
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)
app.add_middleware(
    SessionMiddleware,
    secret_key="ctcl-secret-key-2026"
)
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(
    search_router
)