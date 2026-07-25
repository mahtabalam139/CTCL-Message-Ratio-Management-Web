from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import (
    RedirectResponse,
    FileResponse
)
from fastapi.templating import Jinja2Templates

from services.reports_service import (
    get_reports_page,
    export_users_report,
    export_ctcl_report,
    export_audit_report
)
from datetime import datetime

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/reports")
def reports(request: Request):

    if "user" not in request.session:
        return RedirectResponse("/", status_code=302)

    data = get_reports_page()

    return templates.TemplateResponse(
        request,
        "reports.html",
        {
            "request": request,
            "title": "Reports",
            **data
        }
    )

# ==========================================================
# CTCL REPORT
# ==========================================================

@router.get("/reports/ctcl")
def ctcl_report(request: Request):

    if "user" not in request.session:

        return RedirectResponse("/", status_code=302)

    filename = export_ctcl_report()

    return FileResponse(

        path=filename,

        filename=filename,

        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )
# ==========================================================
# AUDIT REPORT
# ==========================================================

@router.get("/reports/audit")
def audit_report(request: Request):

    if "user" not in request.session:

        return RedirectResponse("/", status_code=302)

    filename = export_audit_report()

    return FileResponse(

        path=filename,

        filename=filename,

        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )

@router.get("/reports/audit")
def audit_report(request: Request):

    if "user" not in request.session:
        return RedirectResponse("/", status_code=302)

    return templates.TemplateResponse(
        request,
        "reports.html",
        {
            "request": request,
            "title": "Audit Logs Report",
            "coming_soon": "Audit Logs Report"
        }
    )

# ==========================================================
# USERS REPORT
# ==========================================================
@router.get("/reports/users")
def users_report(request: Request):

    if "user" not in request.session:

        return RedirectResponse("/", status_code=302)

    filename = export_users_report()

    return FileResponse(

        path=filename,

        filename = f"Users_Report_{datetime.now():%Y%m%d_%H%M%S}.xlsx",

        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )