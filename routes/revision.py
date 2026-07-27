from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from services.revision_service import (
    get_revision_record,
    preview_revision,
    save_revision
)

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# ==========================================================
# REVISION PAGE
# ==========================================================

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


# ==========================================================
# PREVIEW
# ==========================================================

@router.post("/revision/{record_id}")
def revision_preview(
    request: Request,
    record_id: int,
    scenario: str = Form(...),
    cm_msg: int = Form(...),
    fo_msg: int = Form(...),
    cd_msg: int = Form(...),
    msg_line: int = Form(...),
    comments: str = Form(""),
    start_date: str = Form(...)
):

    if "user" not in request.session:

        return RedirectResponse(
            "/",
            status_code=302
        )


    result = preview_revision(
        record_id=record_id,
        scenario=scenario,
        cm_msg=cm_msg,
        fo_msg=fo_msg,
        cd_msg=cd_msg,
        msg_line=msg_line,
        comments=comments,
        start_date=start_date
    )
    print(result)


    return templates.TemplateResponse(
        request,
        "revision.html",
        {
            "request": request,
            "title": "Revision",
            "record": result.get("new_record"),
            "current_record": result.get("current_record"),
            "show_preview": result.get("show_preview", False),
            "error": result.get("error")
        }
    )


# ==========================================================
# CONFIRM REVISION
# ==========================================================

@router.post("/confirm-revision")
def confirm_revision(

    request: Request,

    record_id: int = Form(...),

    scenario: str = Form(...),

    cm_msg: int = Form(...),

    fo_msg: int = Form(...),

    cd_msg: int = Form(...),

    msg_line: int = Form(...),

    comments: str = Form(...),
    start_date: str = Form(...)

):

    if "user" not in request.session:

        return RedirectResponse(
            "/",
            status_code=302
        )

    # print("\n========== CONFIRM REVISION ==========")
    print("ID :", record_id)
    print("Scenario :", scenario)
    print("CM :", cm_msg)
    print("FO :", fo_msg)
    print("CD :", cd_msg)
    print("Msg :", msg_line)
    print("Comments :", comments)
    # print("======================================")
    print("START DATE =", start_date)
    print(type(start_date))
    username = request.session["user"]["username"]
    save_revision(
    username=username,

    record_id=record_id,

    scenario=scenario,

    cm_msg=cm_msg,

    fo_msg=fo_msg,

    cd_msg=cd_msg,

    msg_line=msg_line,

    comments=comments,

    start_date=start_date

)
    request.session["success"] = "Revision saved successfully."

    return RedirectResponse(
        "/search",
        status_code=303
    )