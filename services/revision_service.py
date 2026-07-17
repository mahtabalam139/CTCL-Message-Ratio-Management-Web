


from excel_handler import get_record_by_id
from validation import validate_revision_form


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
    comments
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
        return {
        "error": error,
        "id": record_id,
        "Scenario": scenario,
        "CM Msgs": cm_msg,
        "Fo Msgs": fo_msg,
        "CD Msgs": cd_msg,
        "Msg Line": msg_line,
        "Comments": comments
    }

    print("\n========== REVISION PREVIEW ==========")
    print("ID        :", record_id)
    print("Scenario  :", scenario)
    print("CM Msg    :", cm_msg)
    print("FO Msg    :", fo_msg)
    print("CD Msg    :", cd_msg)
    print("Msg Line  :", msg_line)
    print("Comments  :", comments)
    print("======================================\n")

    return {
        "id": record_id,
        "Scenario": scenario,
        "CM Msgs": cm_msg,
        "Fo Msgs": fo_msg,
        "CD Msgs": cd_msg,
        "Msg Line": msg_line,
        "Comments": comments
    }