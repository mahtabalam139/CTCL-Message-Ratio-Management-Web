from db_handler import insert_new_record
from date_utils import (
    parse_date,
    format_date,
    get_month_end
)
from datetime import datetime
from services.audit_logs_service import (
    save_audit_log
)
from validation import validate_add_record_form

# ==========================================================
# LOAD ADD RECORD PAGE
# ==========================================================

def get_add_page():

    return {
        "show_preview": False
    }


# ==========================================================
# ADD RECORD PREVIEW
# ==========================================================

def preview_add_record(

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
    error = validate_add_record_form(

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
    if error:

        return {
            "show_preview": False,
            "error": error
        }
    start = datetime.strptime(
        start_date,
        "%Y-%m-%d"
    ).date()

    end = get_month_end(start)

    return {

        "show_preview": True,

        "preview": {

            "Env": env,
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

            "CM Msgs": cm_msg,
            "Fo Msgs": fo_msg,
            "CD Msgs": cd_msg,

            "Msg Line": msg_line,

            "Start Date": format_date(start),
            "End Date": format_date(end),

            "Comments": comments

        }

    }
# ==========================================================
# SAVE ADD RECORD
# ==========================================================

from db_handler import insert_new_record


def save_add_record(

    username,

    preview

):


    insert_new_record(preview)
    save_audit_log(

    username=username,

    module="CTCL",

    action="Add Record",

    description=(

        f"New CTCL record added "

        f"(Exchange IP: {preview['Exchange IP']}, "

        f"Dealer ID: {preview['Dealer ID']})"

    )

)

