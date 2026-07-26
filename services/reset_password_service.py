from db_handler import (
    get_user_by_username,
    update_password
)

# ==========================================================
# GET USER
# ==========================================================

def get_reset_user(username):

    # print("\n========== GET USER ==========")
    # print("USERNAME =", username)

    user = get_user_by_username(username)

    if user is None:

        # print("USER NOT FOUND")

        return None

    # print("USER FOUND")

    return user


# ==========================================================
# PREVIEW RESET PASSWORD
# ==========================================================

def validate_password(

    username,

    password,

    confirm_password

):

    if not password.strip():

        return "Password cannot be empty."

    if password != confirm_password:

        return "Passwords do not match."

    user = get_user_by_username(username)

    if user is None:

        return "User not found."

    return None

# ==========================================================
# PREVIEW RESET PASSWORD
# ==========================================================

def preview_reset_password(
    username,
    password,
    confirm_password
):

    user = get_reset_user(
        username
    )

    error = validate_password(

        username,

        password,

        confirm_password

    )

    if error:

        return {

            "user": user,

            "error": error,

            "show_preview": False

        }

    return {

        "user": user,

        "password": password,

        "show_preview": True

    }
# ==========================================================
# CONFIRM RESET PASSWORD
# ==========================================================

def confirm_reset_password(

    username,
    password

):

    update_password(

        username,
        password

    )

    print("PASSWORD RESET SUCCESSFULLY")