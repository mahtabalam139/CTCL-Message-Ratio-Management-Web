
from tkinter import messagebox
import pandas as pd

from date_utils import parse_date
from constants import VALID_MESSAGE_CATEGORIES

# ---------------------- REVISION VALIDATION START ------------------------------
def validate_revision_values(
        new_scenario,
        new_cm_msgs,
        new_fo_msgs,
        new_cd_msgs,
        new_msg_line,
        new_comments
):

    if not new_scenario.strip():

        messagebox.showerror(
            "Validation Error",
            "Scenario cannot be blank"
        )
        return False

    if not new_comments.strip():

        messagebox.showerror(
            "Validation Error",
            "Comments cannot be blank"
        )
        return False

    try:

        cm = int(new_cm_msgs)
        fo = int(new_fo_msgs)
        cd = int(new_cd_msgs)

        calculated_total = cm + fo + cd

        if int(new_msg_line) not in VALID_MESSAGE_CATEGORIES:

            messagebox.showerror(
                "Validation Error",
                "Invalid Message Category"
            )
            return False

        if calculated_total != int(new_msg_line):

            messagebox.showerror(
                "Validation Error",
                "Message Line mismatch detected"
            )
            return False

        if cm < 0 or fo < 0 or cd < 0:

            messagebox.showerror(
                "Validation Error",
                "Message values cannot be negative"
            )
            return False

    except ValueError:

        messagebox.showerror(
            "Validation Error",
            "Message values must be numeric"
        )
        return False

    return True

# ---------------------- REVISION VALIDATION END ------------------------------
def validate_revision_form(
    scenario,
    cm_msg,
    fo_msg,
    cd_msg,
    msg_line,
    comments
):

    if not scenario.strip():
        return "Scenario cannot be blank."

    if not comments.strip():
        return "Comments cannot be blank."

    try:

        cm = int(cm_msg)
        fo = int(fo_msg)
        cd = int(cd_msg)
        line = int(msg_line)

    except ValueError:

        return "Message values must be numeric."

    if cm < 0 or fo < 0 or cd < 0:

        return "Message values cannot be negative."

    if line not in VALID_MESSAGE_CATEGORIES:

        return "Invalid Message Category."

    if (cm + fo + cd) != line:

        return "CM + FO + CD must equal Msg Line."

    return None

def validate_duplicate_revision(
    current_record,
    scenario,
    cm_msg,
    fo_msg,
    cd_msg,
    msg_line,
    comments
):
    return None  # Placeholder for future implementation of duplicate revision validation