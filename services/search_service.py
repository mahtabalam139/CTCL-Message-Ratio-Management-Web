
from excel_handler import search_records
from excel_handler import get_latest_record


def get_search_result(
        search_type,
        search_value
):
    """
    Search CTCL records and return:
    1. Latest Active Record (dict)
    2. Complete Revision History (list of dict)
    """

    history_df = search_records(
        search_type,
        search_value
    )

    if history_df.empty:

        return None, []

    latest_record = get_latest_record(
        history_df
    )

    if latest_record is not None:

        latest_record = latest_record.to_dict()

    history = history_df.to_dict(
        orient="records"
    )

    return latest_record, history