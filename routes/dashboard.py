from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from services.dashboard_service import get_dashboard_summary

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/dashboard")
def dashboard(
        request: Request
):

    if "user" not in request.session:

        return RedirectResponse(
            "/",
            status_code=302
        )

    summary = get_dashboard_summary()

    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "request": request,
            "title": "Dashboard",

            "summary": summary
        }
    )