
from db_handler import authenticate_user


def login_user(
        username,
        password
):

    user = authenticate_user(
        username,
        password
    )

    # print("USERNAME =", username)
    # print("PASSWORD =", password)
    # print("USER =", user)

    return user