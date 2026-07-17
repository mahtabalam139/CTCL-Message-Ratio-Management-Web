
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from services.revision_service import get_revision_record
from fastapi import Form
from services.revision_service import preview_revision

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/revision/{record_id}")
def revision_page(
    request: Request,
    record_id: int
):

    if "user" not in request.session:
        return RedirectResponse(
            "/",
            status_code=302
        )

    record = get_revision_record(record_id)

    if record is None:
        return RedirectResponse(
            "/search",
            status_code=302
        )

    return templates.TemplateResponse(
        request,
        "revision.html",
        {
            "request": request,
            "title": "Revision",
            "record": record
        }
    )
@router.post("/revision/{record_id}")
def revision_preview(
        request: Request,
        record_id: int,
        scenario: str = Form(...),
        cm_msg: int = Form(...),
        fo_msg: int = Form(...),
        cd_msg: int = Form(...),
        msg_line: int = Form(...),
        comments: str = Form("")
    ):

        if "user" not in request.session:

            return RedirectResponse(
                "/",
                status_code=302
            )

        record = preview_revision(
            record_id=record_id,
            scenario=scenario,
            cm_msg=cm_msg,
            fo_msg=fo_msg,
            cd_msg=cd_msg,
            msg_line=msg_line,
            comments=comments
        )
        error = record.get("error")

        return templates.TemplateResponse(
        request,
        "revision.html",
        {
            "request": request,
            "title": "Revision",
            "record": record,
            "error": error
        }
    )