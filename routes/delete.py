from urllib import request

from fastapi import APIRouter
from fastapi import Request
from fastapi import Form

from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from services.delete_service import (
    get_delete_record,
    confirm_delete
)

router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


# ==========================================================
# DELETE PAGE
# ==========================================================

@router.get("/delete/{record_id}")
def delete_page(
    request: Request,
    record_id: int
):

    if "user" not in request.session:

        return RedirectResponse(
            "/",
            status_code=302
        )

    record = get_delete_record(record_id)

    if record is None:

        return RedirectResponse(
            "/search",
            status_code=302
        )

    print(record)

    return templates.TemplateResponse(
        request,
        "delete_record.html",
        {
            "request": request,
            "title": "Delete Record",
            "record": record
        }
    )


# ==========================================================
# CONFIRM DELETE
# ==========================================================

@router.post("/confirm-delete")
def confirm_delete_record(

    request: Request,

    record_id: int = Form(...)

):

    if "user" not in request.session:

        return RedirectResponse(
            "/",
            status_code=302
        )
    print("RECORD ID =", record_id)

    result = confirm_delete(record_id)

    if result:

        request.session["error_message"] = result

    else:

        request.session["success_message"] = (
            "CTCL record deleted successfully."
        )

    return RedirectResponse(
        "/search",
        status_code=303
)