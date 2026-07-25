from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/reports")
def reports(request: Request):

    if "user" not in request.session:

        return RedirectResponse("/", status_code=302)

    return templates.TemplateResponse(
        request,
        "reports.html",
        {
            "request": request,
            "title": "Reports"
        }
    )