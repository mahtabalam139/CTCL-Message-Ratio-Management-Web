
from db_handler import (
    get_record_by_id,
    get_revision_history,
    restore_end_date,
    delete_record
)

# ==========================================================
# GET DELETE RECORD
# ==========================================================

def get_delete_record(
    record_id
):
    # print("RECORD ID =", record_id)

    record = get_record_by_id(
        record_id
    )

    if record is None:

        # print("RECORD NOT FOUND")

        return None

    # print("RECORD FOUND")

    return record




def confirm_delete(record_id):

    record = get_record_by_id(record_id)

    if record is None:

        raise Exception("Record not found.")

    history = get_revision_history(
        record["exchange_ip"]
    )

    if not history:

        raise Exception(
            "Revision history not found."
        )

    print("TOTAL REVISIONS =", len(history))

    if len(history) < 2:

        # print("DELETE BLOCKED : Only one revision exists.")

        return "Cannot delete the only active revision."

    latest_record = history[-1]

    if latest_record["id"] != record_id:

        # print("DELETE BLOCKED : Not latest revision.")

        return "Only the latest active revision can be deleted."

    previous_record = history[-2]

    print("PREVIOUS RECORD =", previous_record["id"])
    print("LATEST RECORD   =", latest_record["id"])

    restore_end_date(

        previous_record["id"],
        latest_record["end_date"]

    )

    delete_record(record_id)

    # print("DELETE COMPLETED")
    
    return None