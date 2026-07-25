
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from routes.dashboard import router as dashboard_router
from routes.search import router as search_router
from routes.delete import router as delete_router
from routes.audit_logs import router as audit_logs_router
from routes.auth import router as auth_router
from routes import revision
from routes.add_record import router as add_router
from routes.reports import router as reports_router
from routes.users import router as users_router
app = FastAPI(
    title="CTCL Message Ratio Management Tool"
)
from routes.reset_password import (
    router as reset_password_router
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
app.include_router(search_router)
app.include_router(add_router)
app.include_router(delete_router)
app.include_router(users_router)
app.include_router(reset_password_router)
app.include_router(audit_logs_router)
app.include_router(reports_router)