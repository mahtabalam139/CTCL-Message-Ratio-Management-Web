from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from services.audit_logs_service import (
    fetch_audit_logs
)

router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


# ==========================================================
# AUDIT LOGS
# ==========================================================

@router.get("/audit")
def audit_logs(
    request: Request
):

    if "user" not in request.session:

        return RedirectResponse(
            "/",
            status_code=302
        )

    logs = fetch_audit_logs()

    return templates.TemplateResponse(

        request,

        "audit_logs.html",

        {

            "request": request,

            "title": "Audit Logs",

            "logs": logs

        }

    )