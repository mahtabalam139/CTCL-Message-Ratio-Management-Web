

import pandas as pd

from datetime import datetime

from date_utils import parse_date
from constants import VALID_MESSAGE_CATEGORIES

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

# ==========================================================
# ADD RECORD VALIDATION
# ==========================================================

def validate_add_record_form(
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
):

    mandatory_fields = {

        "Environment": env,
        "Exchange": exchange,
        "Location": location,
        "Dedicated": dedicated,
        "System": system,
        "Server IP": server_ip,
        "Exchange IP": exchange_ip,
        "FO CTCL": fo_ctcl,
        "CM CTCL": cm_ctcl,
        "CDS CTCL": cds_ctcl,
        "Dealer ID": dealer_id,
        "Rack": rack,
        "Scenario": scenario,
        "Start Date": start_date,
        "Comments": comments

    }

    for field, value in mandatory_fields.items():

        if not str(value).strip():

            return f"{field} cannot be blank."

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
    try:

        datetime.strptime(
                start_date,
                "%Y-%m-%d"
            )

    except ValueError:

        return "Invalid Start Date."

    return None