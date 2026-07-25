from urllib import request

from fastapi import APIRouter
from fastapi import Request
from fastapi import Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from services.add_record_service import (
    get_add_page,
    preview_add_record,
    save_add_record
)

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# ==========================================================
# ADD RECORD PAGE
# ==========================================================

@router.get("/add")
def add_record_page(request: Request):

    if "user" not in request.session:

        return RedirectResponse(
            "/",
            status_code=302
        )

    data = get_add_page()

    return templates.TemplateResponse(
        request,
        "add_record.html",
        {
            "request": request,
            "title": "Add Record",
            **data
        }
    )


# ==========================================================
# ADD RECORD PREVIEW
# ==========================================================

@router.post("/add")
def add_record_preview(

    
    request: Request,
    env: str = Form(...),
    exchange: str = Form(...),
    location: str = Form(...),
    dedicated: str = Form(...),
    system: str = Form(...),
    server_ip: str = Form(...),
    exchange_ip: str = Form(...),
    fo_ctcl: str = Form(...),
    cm_ctcl: str = Form(...),
    cds_ctcl: str = Form(...),
    dealer_id: str = Form(...),
    rack: str = Form(...),

    scenario: str = Form(...),

    cm_msg: int = Form(...),
    fo_msg: int = Form(...),
    cd_msg: int = Form(...),

    msg_line: int = Form(0),

    start_date: str = Form(...),

    comments: str = Form("")

):
    scenario_map = {
        "A2": 40,
        "B1": 100,
        "C1": 200,
        "D1": 400,
        "E1": 1000
    }

    msg_line = scenario_map.get(scenario, msg_line)

    print("Calculated Msg Line :", msg_line)

    result = preview_add_record(

        env,
        exchange,
        location,
        dedicated,
        system,
        server_ip,
        exchange_ip,
        fo_ctcl,
        cm_ctcl,
        cds_ctcl,
        dealer_id,
        rack,
        scenario,
        cm_msg,
        fo_msg,
        cd_msg,
        msg_line,
        start_date,
        comments
    )
    if result.get("show_preview"):
        request.session["add_preview"] = result["preview"]

    return templates.TemplateResponse(
        request,
        "add_record.html",
        {
            "request": request,
            "title": "Add Record",

            "error": result.get("error"),

            **result
        }
    )
# ==========================================================
# CONFIRM ADD RECORD
# ==========================================================

@router.post("/confirm-add")
def confirm_add_record(request: Request):

    preview = request.session.get("add_preview")

    if not preview:
        return RedirectResponse(
            "/add",
            status_code=302
        )
    username = request.session["user"]
    save_add_record(

        username=username,

        preview=preview

    )
    request.session["success_message"] = (
    "CTCL record added successfully."
)
    request.session.pop("add_preview", None)

    return RedirectResponse(
        "/search",
        status_code=303
    )