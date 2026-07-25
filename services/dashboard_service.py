from db_handler import (
    get_total_records,
    get_active_records,
    get_total_users,
    get_total_revisions,
    get_recent_revisions
)

def get_dashboard_summary():

    return {

        "total_records": get_total_records(),

        "active_records": get_active_records(),

        "total_users": get_total_users(),

        "today_revisions": get_total_revisions(),

        "recent_revisions": get_recent_revisions()

    }