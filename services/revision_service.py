


from excel_handler import (
    get_record_by_id,
    check_duplicate_revision,
    save_revision_record
)

from validation import validate_revision_form

from date_utils import parse_date
from datetime import datetime
from services.audit_logs_service import (
    save_audit_log
)


def get_revision_record(record_id):

    record = get_record_by_id(record_id)

    if record is None:
        return None

    return record.to_dict()
    

def preview_revision(
    record_id,
    scenario,
    cm_msg,
    fo_msg,
    cd_msg,
    msg_line,
    comments,
    start_date
):

    error = validate_revision_form(
        scenario,
        cm_msg,
        fo_msg,
        cd_msg,
        msg_line,
        comments
    )

    if error:

        print(error)
        current_record = get_revision_record(record_id)

        return {
            "current_record": current_record,
            "new_record": {
                "id": record_id,
                "Scenario": scenario,
                "CM Msgs": cm_msg,
                "Fo Msgs": fo_msg,
                "CD Msgs": cd_msg,
                "Msg Line": msg_line,
                "Comments": comments,
                "Start Date": start_date,
                "End Date": current_record["End Date"]
            },
            "show_preview": True
        }

    duplicate = check_duplicate_revision(
        get_revision_record(record_id),
        scenario,
        cm_msg,
        fo_msg,
        cd_msg,
        msg_line,
        comments
    )

    if duplicate:

        return {
            "error": "No changes detected. Duplicate revision.",
            "new_record": {
                "id": record_id,
                "Scenario": scenario,
                "CM Msgs": cm_msg,
                "Fo Msgs": fo_msg,
                "CD Msgs": cd_msg,
                "Msg Line": msg_line,
                "Comments": comments,
                "Start Date": start_date
            },
            "show_preview": False
        }
    current_record = get_revision_record(record_id)

    new_end_date = current_record["End Date"]
    return {
        "current_record": get_revision_record(record_id),
        "new_record": {
            "id": record_id,
            "Scenario": scenario,
            "CM Msgs": cm_msg,
            "Fo Msgs": fo_msg,
            "CD Msgs": cd_msg,
            "Msg Line": msg_line,
            "Comments": comments,
            "Start Date": start_date,
            "End Date": new_end_date
        },
        "show_preview": True
    }
# ==========================================================
# FUNCTION : save_revision START
# ==========================================================

def save_revision(
    username,
    record_id,
    scenario,
    cm_msg,
    fo_msg,
    cd_msg,
    msg_line,
    comments,
    start_date
):

    active_record = get_record_by_id(
        record_id
    )

    if active_record is None:

        raise Exception(
            "Record not found."
        )

    request_date = datetime.strptime(
        start_date,
        "%Y-%m-%d"
    ).date()
    print("REQUEST DATE =", request_date)
    print(type(request_date))

    save_revision_record(
        active_record=active_record,
        request_date=request_date,
        new_scenario=scenario,
        new_cm_msgs=cm_msg,
        new_fo_msgs=fo_msg,
        new_cd_msgs=cd_msg,
        new_msg_line=msg_line,
        new_comments=comments
    )
    save_audit_log(

    username=username,

    module="CTCL",

    action="Save Revision",

    description=(

        f"Exchange IP: {active_record['Exchange IP']}, "

        f"Scenario: {active_record['Scenario']} -> {scenario}, "

        f"Msg Line: {active_record['Msg Line']} -> {msg_line}"

    )

)

    print("REVISION SAVED SUCCESSFULLY")

    return True

# ==========================================================
# FUNCTION : save_revision END
# ==========================================================