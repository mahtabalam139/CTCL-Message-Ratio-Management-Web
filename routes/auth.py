
from db_handler import insert_audit_log
from fastapi import APIRouter
from fastapi import Form
from fastapi import Request

from fastapi.responses import RedirectResponse

from fastapi.templating import Jinja2Templates

from services.auth_service import login_user

router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


@router.get("/")
def login_page(
        request: Request
):

    return templates.TemplateResponse(
        request,
        "login.html",
        {
            "request": request,
            "title": "CTCL Login"
        }
    )


@router.post("/")
def login(
        request: Request,
        username: str = Form(...),
        password: str = Form(...)
):

    user = login_user(
        username,
        password
    )

    if user is None:

        return templates.TemplateResponse(
            request,
            "login.html",
            {
                "request": request,
                "title": "CTCL Login",
                "error": "Invalid Username or Password"
            }
        )

    request.session["user"] = user["username"]

    request.session["role"] = user["role"]

    request.session["full_name"] = user["full_name"]
    
    insert_audit_log(

    user["username"],

    "WEB",

    "Login",

    "Login",

    f"User '{user['username']}' logged in."

)

    return RedirectResponse(
        "/dashboard",
        status_code=302
    )
@router.get("/logout")
def logout(
    request: Request
):

    username = request.session.get(
        "user"
    )

    if username:

        insert_audit_log(

            username,

            "WEB",

            "Login",

            "Logout",

            f"User '{username}' logged out."

        )

    request.session.clear()

    return RedirectResponse(

        "/",

        status_code=302

    )