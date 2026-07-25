from db_handler import (
    get_all_users,
    create_user,
    user_exists,
    get_user_by_username,
    update_user,
    disable_user_account
)


# ==========================================================
# GET ALL USERS
# ==========================================================

def get_users():

    print("\n========== USERS ==========")

    users = get_all_users()

    print("TOTAL USERS =", len(users))

    return users
# ==========================================================
# PREVIEW USER
# ==========================================================

def preview_user(
    username,
    full_name,
    password,
    role
):

    if not username.strip():

        return {
            "error": "Username cannot be blank."
        }

    if not full_name.strip():

        return {
            "error": "Full Name cannot be blank."
        }

    if not password.strip():

        return {
            "error": "Password cannot be blank."
        }

    if user_exists(username):

        return {
            "error": "Username already exists."
        }

    return {

        "show_preview": True,

        "user": {

            "username": username,
            "full_name": full_name,
            "password": password,
            "role": role

        }

    }


# ==========================================================
# CREATE USER
# ==========================================================

def save_user(user):

    create_user(

        username=user["username"],

        password=user["password"],

        full_name=user["full_name"],

        role=user["role"],

        is_active=1

    )

    print("USER SAVED SUCCESSFULLY")
# ==========================================================
# GET USER
# ==========================================================

def get_user(username):

    print("\n========== GET USER ==========")
    print("USERNAME =", username)

    user = get_user_by_username(
        username
    )

    if user is None:

        print("USER NOT FOUND")

        return None

    print("USER FOUND")

    return user


# ==========================================================
# PREVIEW UPDATE USER
# ==========================================================

def preview_update_user(

    username,
    full_name,
    role,
    is_active

):

    if not full_name.strip():

        return {

            "error":
            "Full Name cannot be blank."

        }

    return {

        "show_preview": True,

        "user": {

            "username": username,

            "full_name": full_name,

            "role": role,

            "is_active": is_active

        }

    }


# ==========================================================
# SAVE UPDATED USER
# ==========================================================

def save_updated_user(

    user

):

    update_user(

        username=user["username"],

        full_name=user["full_name"],

        role=user["role"],

        is_active=user["is_active"]

    )

    print("USER UPDATED SUCCESSFULLY")
# ==========================================================
# GET DISABLE USER
# ==========================================================

def get_disable_user(username):

    print("\n========== DISABLE USER ==========")
    print("USERNAME =", username)

    user = get_user_by_username(
        username
    )

    if user is None:

        print("USER NOT FOUND")

        return None

    print("USER FOUND")

    return user


# ==========================================================
# DISABLE USER
# ==========================================================

def disable_user(username):

    print("\n========== CONFIRM DISABLE ==========")
    print("USERNAME =", username)

    disable_user_account(
        username
    )

    print("USER DISABLED SUCCESSFULLY")