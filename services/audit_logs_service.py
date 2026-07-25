from db_handler import (
    insert_audit_log,
    get_audit_logs
)


# ==========================================================
# SAVE AUDIT LOG
# ==========================================================

def save_audit_log(

    username,
    module,
    action,
    description

):

    insert_audit_log(

        username=username,
        source="WEB",
        module=module,
        action=action,
        description=description

    )


# ==========================================================
# GET AUDIT LOGS
# ==========================================================

def fetch_audit_logs():

    return get_audit_logs()