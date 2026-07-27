from fastapi import Request
from fastapi.responses import RedirectResponse


# ==========================================================
# REQUIRE LOGIN
# ==========================================================

def require_login(request: Request):

    user = request.session.get("user")

    if user is None:

        return RedirectResponse(
            "/",
            status_code=302
        )

    return user


# ==========================================================
# REQUIRE ADMIN
# ==========================================================

def require_admin(request: Request):

    user = request.session.get("user")

    if user is None:

        return RedirectResponse(
            "/",
            status_code=302
        )

    if user["role"] != "Admin":

        request.session["error"] = (
            "Access Denied."
        )

        return RedirectResponse(
            "/dashboard",
            status_code=302
        )

    return None