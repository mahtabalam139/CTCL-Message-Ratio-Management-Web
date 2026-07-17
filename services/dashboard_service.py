from excel_handler import load_data


def get_dashboard_summary():

    df = load_data()

    total_records = len(df)

    active_records = len(
        df[df["End Date"].notna()]
    )

    total_users = 0

    today_revisions = 0

    return {
        "total_records": total_records,
        "active_records": active_records,
        "total_users": total_users,
        "today_revisions": today_revisions
    }