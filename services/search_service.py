from db_handler import (
    search_records_db
)


# ==========================================================
# SEARCH RESULT
# ==========================================================

def get_search_result(
    search_type,
    search_value
):

    history = search_records_db(

        search_type,
        search_value

    )

    if not history:

        return None, []

    latest_record = history[0]

    return latest_record, history