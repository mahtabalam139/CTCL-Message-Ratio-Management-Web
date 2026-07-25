from fastapi import APIRouter
from fastapi import Request
from fastapi import Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from services.reset_password_service import (
    get_reset_user,
    preview_reset_password,
    confirm_reset_password
)

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# ==========================================================
# RESET PASSWORD PAGE
# ==========================================================

@router.get("/reset-password/{username}")
def reset_password_page(
    request: Request,
    username: str
):

    if "user" not in request.session:

        return RedirectResponse(
            "/",
            status_code=302
        )

    user = get_reset_user(username)

    if user is None:

        return RedirectResponse(
            "/users",
            status_code=302
        )

    return templates.TemplateResponse(
        request,
        "reset_password.html",
        {
            "request": request,
            "title": "Reset Password",
            "user": user,
            "show_preview": False
        }
    )


# ==========================================================
# RESET PASSWORD PREVIEW
# ==========================================================

@router.post("/reset-password/{username}")
def reset_password_preview(
    request: Request,
    username: str,
    password: str = Form(...),
    confirm_password: str = Form(...)
):

    if "user" not in request.session:

        return RedirectResponse(
            "/",
            status_code=302
        )

    result = preview_reset_password(
        username,
        password,
        confirm_password
    )
    print("\n========== RESET PASSWORD PREVIEW ==========")
    print("USERNAME =", username)
    print("SHOW PREVIEW =", result["show_preview"])

    if result.get("error"):

        print("ERROR =", result["error"])

    print("===========================================\n")

    if result["show_preview"]:

        request.session["reset_password"] = {

            "username": username,
            "password": password

        }

    return templates.TemplateResponse(
        request,
        "reset_password.html",
        {
            "request": request,
            "title": "Reset Password",
            **result
        }
    )


# ==========================================================
# CONFIRM RESET PASSWORD
# ==========================================================

@router.post("/confirm-reset-password")
def confirm_password(
    request: Request
):

    if "user" not in request.session:

        return RedirectResponse(
            "/",
            status_code=302
        )

    data = request.session.get(
        "reset_password"
    )

    if not data:

        return RedirectResponse(
            "/users",
            status_code=302
        )
    print("\n========== CONFIRM PASSWORD RESET ==========")
    print("USERNAME =", data["username"])
    print("===========================================\n")
    confirm_reset_password(

        data["username"],
        data["password"]

    )

    request.session.pop(
        "reset_password",
        None
    )

    request.session["success"] = (
        "Password reset successfully."
    )

    return RedirectResponse(
        "/users",
        status_code=303
    )