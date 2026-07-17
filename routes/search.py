
from fastapi import APIRouter
from fastapi import Request
from fastapi import Form

from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from services.search_service import get_search_result


router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


@router.get("/search")
def search_page(
        request: Request
):

    if "user" not in request.session:

        return RedirectResponse(
            "/",
            status_code=302
        )

    return templates.TemplateResponse(
        request,
        "search.html",
        {
            "request": request,
            "title": "Search Records",

            "latest": None,
            "history": [],

            "search_type": "",
            "search_value": ""
        }
    )


@router.post("/search")
def search_record(
        request: Request,
        search_type: str = Form(...),
        search_value: str = Form(...)
):

    if "user" not in request.session:

        return RedirectResponse(
            "/",
            status_code=302
        )

    latest_record, history = get_search_result(
        search_type,
        search_value
    )

    return templates.TemplateResponse(
        request,
        "search.html",
        {
            "request": request,
            "title": "Search Records",

            "latest": latest_record,
            "history": history,

            "search_type": search_type,
            "search_value": search_value
        }
    )