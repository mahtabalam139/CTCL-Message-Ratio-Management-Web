from fastapi import APIRouter
from fastapi import Request
from fastapi import Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from services.auth_helper import require_admin

from services.user_service import (

    get_users,
    preview_user,
    save_user,
    get_user,
    preview_update_user,
    save_updated_user,
    get_disable_user,
    disable_user

)

router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


# ==========================================================
# USERS PAGE
# ==========================================================

@router.get("/users")
def users_page(request: Request):

    result = require_admin(request)

    if result:
        return result

    users = get_users()

    return templates.TemplateResponse(
        request,
        "users.html",
        {
            "request": request,
            "title": "User Management",
            "users": users
        }
    )
# ==========================================================
# ADD USER PAGE
# ==========================================================

@router.get("/add-user")
def add_user_page(request: Request):

    result = require_admin(request)

    if result:
        return result

    return templates.TemplateResponse(
        request,
        "add_user.html",
        {
            "request": request,
            "title": "Add User"
        }
    )
# ==========================================================
# USER PREVIEW
# ==========================================================

@router.post("/add-user")
def add_user_preview(

    request: Request,

    username: str = Form(...),

    full_name: str = Form(...),

    password: str = Form(...),

    role: str = Form(...)

):

    result = require_admin(request)

    if result:
        return result

    result = preview_user(

        username,
        full_name,
        password,
        role

    )

    if result.get("show_preview"):

        request.session["user_preview"] = result["user"]

    return templates.TemplateResponse(

        request,

        "add_user.html",

        {

            "request": request,

            "title": "Add User",

            **result

        }

    )
# ==========================================================
# CONFIRM USER
# ==========================================================

@router.post("/confirm-user")
def confirm_user(

    request: Request

):

    result = require_admin(request)

    if result:
        return result

    user = request.session.get(
        "user_preview"
    )

    if not user:

        return RedirectResponse(
            "/add-user",
            status_code=302
        )

    save_user(user)

    request.session.pop(
        "user_preview",
        None
    )

    request.session["success"] = (
        "User created successfully."
    )

    return RedirectResponse(

        "/users",

        status_code=303

    )
# ==========================================================
# EDIT USER PAGE
# ==========================================================

@router.get("/edit-user/{username}")
def edit_user_page(

    request: Request,
    username: str

):

    result = require_admin(request)

    if result:
        return result

    user = get_user(username)

    if user is None:

        return RedirectResponse(
            "/users",
            status_code=302
        )

    return templates.TemplateResponse(

        request,

        "edit_user.html",

        {

            "request": request,

            "title": "Edit User",

            "user": user

        }

    )


# ==========================================================
# EDIT USER PREVIEW
# ==========================================================

@router.post("/edit-user/{username}")
def edit_user_preview(

    request: Request,

    username: str,

    full_name: str = Form(...),

    role: str = Form(...),

    is_active: int = Form(...)

):

    result = require_admin(request)

    if result:
        return result

    result = preview_update_user(

        username,

        full_name,

        role,

        is_active

    )

    if result.get("show_preview"):

        request.session["edit_user"] = result["user"]

    return templates.TemplateResponse(

        request,

        "edit_user.html",

        {

            "request": request,

            "title": "Edit User",

            **result

        }

    )


# ==========================================================
# CONFIRM USER UPDATE
# ==========================================================

@router.post("/confirm-edit-user")
def confirm_edit_user(

    request: Request

):

    result = require_admin(request)

    if result:
        return result

    user = request.session.get(
        "edit_user"
    )

    if not user:

        return RedirectResponse(
            "/users",
            status_code=302
        )

    save_updated_user(user)

    request.session.pop(
        "edit_user",
        None
    )

    request.session["success"] = (
        "User updated successfully."
    )

    return RedirectResponse(

        "/users",

        status_code=303

    )
# ==========================================================
# DISABLE USER PAGE
# ==========================================================

@router.get("/disable-user/{username}")
def disable_user_page(

    request: Request,
    username: str

):

    result = require_admin(request)

    if result:
        return result

    user = get_disable_user(
        username
    )

    if user is None:

        return RedirectResponse(
            "/users",
            status_code=302
        )

    return templates.TemplateResponse(

        request,

        "disable_user.html",

        {

            "request": request,

            "title": "Disable User",

            "user": user

        }

    )


# ==========================================================
# CONFIRM DISABLE USER
# ==========================================================

@router.post("/confirm-disable-user")
def confirm_disable_user(

    request: Request,

    username: str = Form(...)

):

    result = require_admin(request)

    if result:
        return result

    disable_user(
        username
    )

    request.session["success"] = (
        "User disabled successfully."
    )

    return RedirectResponse(

        "/users",

        status_code=303

    )