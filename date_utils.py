import pandas as pd

from datetime import datetime
from datetime import timedelta


# ==========================================================
# Normalize Date Column
# ==========================================================

def normalize_date_column(series):

    result = []

    for value in series:

        if pd.isna(value) or str(value).strip() == "":
            result.append("")
            continue

        value = str(value).strip()

        try:

            dt = datetime.strptime(
                value,
                "%d-%m-%Y"
            )

            result.append(
                dt.strftime("%d-%m-%Y")
            )

            continue

        except:
            pass

        try:

            dt = pd.to_datetime(
                value,
                errors="coerce"
            )

            if pd.notna(dt):

                result.append(
                    dt.strftime("%d-%m-%Y")
                )

            else:

                result.append("")

        except:

            result.append("")

    return pd.Series(result)


# ==========================================================
# Parse Date
# ==========================================================

def parse_date(value):

    return pd.to_datetime(
        value,
        format="%d-%m-%Y",
        dayfirst=True,
        errors="coerce"
    )


# ==========================================================
# Format Date
# ==========================================================

def format_date(date_value):

    if pd.isna(date_value):
        return ""

    return pd.to_datetime(
        date_value
    ).strftime("%d-%m-%Y")


# ==========================================================
# Calculate Effective Date
# Current Rule:
# Mon-Thu  -> Next Day
# Friday   -> Monday
# Saturday -> Monday
# Sunday   -> Monday
# ==========================================================

def calculate_effective_date(request_date):

    weekday = request_date.weekday()

    if weekday == 4:
        return request_date + timedelta(days=3)

    elif weekday == 5:
        return request_date + timedelta(days=2)

    elif weekday == 6:
        return request_date + timedelta(days=1)

    else:
        return request_date + timedelta(days=1)


# ==========================================================
# Get Month End
# ==========================================================

def get_month_end(date_value):

    month_end = pd.Timestamp(date_value) + pd.offsets.MonthEnd(0)

    return month_end.date()


# ==========================================================
# Get Latest Record
# ==========================================================

def get_latest_record(df):

    if len(df) == 0:
        return None

    temp_df = df.copy()

    temp_df["End Date"] = pd.to_datetime(
        temp_df["End Date"],
        format="%d-%m-%Y",
        errors="coerce"
    )

    temp_df = temp_df.sort_values(
        by="End Date",
        ascending=False
    )

    latest_index = temp_df.index[0]

    return df.loc[latest_index]