
from multiprocessing.dummy import connection

import pandas as pd
import os
import shutil
from datetime import datetime
from db_handler import (
    get_cursor,
    update_end_date,
    insert_new_record,
    restore_end_date,
    delete_record
)



from date_utils import (
    normalize_date_column,
    parse_date,
    format_date,
    calculate_effective_date,
    get_month_end
)
from config import (
    EXCEL_FILE,
    BACKUP_FOLDER
)

print("IMPORT PANDAS DONE")
print("IMPORT OPENPYXL DONE")


# =========================================df.rename(columns=================
# FUNCTION : load_data START
# ==========================================================

def load_data():

  
    connection, cursor = get_cursor()
    
    cursor.execute(
        "SELECT * FROM ctcl_message_ratio"
    )
    rows = cursor.fetchall()
    
    columns = [
        column[0]
        for column in cursor.description
    ]
    df = pd.DataFrame(
        rows,
        columns=columns
    )
    cursor.close()
    connection.close()
    df = df.rename(
        columns={
            "env": "Env",
            "exchange_name": "Exchange",
            "location": "Location",
            "dedicated": "Dedicated",
            "system_name": "System",
            "server_ip": "Server IP",
            "exchange_ip": "Exchange IP",
            "fo_ctcl": "FO CTCL",
            "cm_ctcl": "CM CTCL",
            "cds_ctcl": "CDS CTCL",
            "dealer_id": "Dealer ID",
            "rack": "Rack",
            "scenario": "Scenario",
            "cm_msgs": "CM Msgs",
            "fo_msgs": "Fo Msgs",
            "cd_msgs": "CD Msgs",
            "msg_line": "Msg Line",
            "start_date": "Start Date",
            "end_date": "End Date",
            "comments": "Comments"
        }
    )
    df = df.fillna("")

    for col in ["Start Date", "End Date"]:

        df[col] = normalize_date_column(df[col])

    
    print(df.columns.tolist())

    return df

# ==========================================================
# FUNCTION : load_data END
# ==========================================================
# ==========================================================
# FUNCTION : save_excel START
# ==========================================================

def save_excel(df):

    df.to_excel(
        EXCEL_FILE,
        index=False
    )

    

# ==========================================================
# FUNCTION : save_excel END
# ==========================================================

# ==========================================================
# FUNCTION : search_records START
# ==========================================================

def search_records(search_type, search_value):

    print("Searching :", search_type, search_value)

    df = load_data()

    result = df[
        df[search_type]
        .astype(str)
        .str.strip()
        ==
        str(search_value).strip()
    ]

    print("Records Found :", len(result))

    return result

# ==========================================================
# FUNCTION : search_records END
# ==========================================================
# ==========================================================
# FUNCTION : get_record_by_id START
# ==========================================================

def get_record_by_id(record_id):

    df = load_data()

    result = df[
        df["id"] == record_id
    ]

    if result.empty:

        return None

    return result.iloc[0]

# ==========================================================
# FUNCTION : get_record_by_id END
# ==========================================================
# ==========================================================
# FUNCTION : get_latest_record START
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

# ==========================================================
# FUNCTION : get_latest_record END
# ==========================================================

# ==========================================================
# FUNCTION : validate_overlap START
# ==========================================================

def validate_overlap(
    exchange_ip,
    start_date,
    end_date,
    exclude_row=None
):

    df = load_data()

    target_rows = df[
        df["Exchange IP"]
        .astype(str)
        .str.strip()
        ==
        str(exchange_ip).strip()
    ]

    for idx, row in target_rows.iterrows():

        if exclude_row is not None and idx == exclude_row:
            continue

        existing_start = parse_date(
            row["Start Date"]
        )

        existing_end = parse_date(
            row["End Date"]
        )

        if pd.isna(existing_start) or pd.isna(existing_end):
            continue

        existing_start = existing_start.date()
        existing_end = existing_end.date()

        if (
            start_date <= existing_end
            and
            end_date >= existing_start
        ):
            return True

    return False

# ==========================================================
# FUNCTION : validate_overlap END
# ==========================================================


# ==========================================================
# FUNCTION : backup_excel START
# ==========================================================

def backup_excel():

    backup_dir = BACKUP_FOLDER

    if not os.path.exists(backup_dir):

        os.makedirs(backup_dir)

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_file = (
        f"{backup_dir}/CTCL-Jul-2026_{timestamp}.xlsx"
    )

    shutil.copy(
        EXCEL_FILE,
        backup_file
    )

 

    return backup_file

# ==========================================================
# FUNCTION : backup_excel END
# ==========================================================

# ==========================================================
# FUNCTION : check_duplicate_revision START
# ==========================================================

def check_duplicate_revision(
    active_record,
    new_scenario,
    new_cm_msgs,
    new_fo_msgs,
    new_cd_msgs,
    new_msg_line,
    new_comments
):

    if str(active_record.get("Scenario", "")).strip() != str(new_scenario).strip():
        return False

    if str(active_record.get("CM Msgs", "")).strip() != str(new_cm_msgs).strip():
        return False

    if str(active_record.get("Fo Msgs", "")).strip() != str(new_fo_msgs).strip():
        return False

    if str(active_record.get("CD Msgs", "")).strip() != str(new_cd_msgs).strip():
        return False

    if str(active_record.get("Msg Line", "")).strip() != str(new_msg_line).strip():
        return False

    if str(active_record.get("Comments", "")).strip() != str(new_comments).strip():
        return False

    return True

# ==========================================================
# FUNCTION : check_duplicate_revision END
# ==========================================================


# ==========================================================
# FUNCTION : add_new_record START
# ==========================================================

def add_new_record(record):

    df = load_data()

    new_row = pd.DataFrame([record])

    df = pd.concat(
        [df, new_row],
        ignore_index=True
    )
    insert_new_record(record)
    save_excel(df)

    print("NEW RECORD SAVED")
    print("TOTAL ROWS AFTER APPEND =", len(df))

# ==========================================================
# FUNCTION : add_new_record END
# ==========================================================


# ==========================================================
# FUNCTION : save_revision_record START
# ==========================================================

def save_revision_record(
    active_record,
    request_date,
    new_scenario,
    new_cm_msgs,
    new_fo_msgs,
    new_cd_msgs,
    new_msg_line,
    new_comments
):

    df = load_data()
    connection, cursor = get_cursor()

    row_index = active_record.name

    current_end_date = parse_date(
        df.loc[row_index, "End Date"]
    )

    exchange_ip = str(
        active_record["Exchange IP"]
    ).strip()

    ip_rows = df[
        df["Exchange IP"]
        .astype(str)
        .str.strip()
        ==
        exchange_ip
    ]

    max_end_date = parse_date(
        ip_rows["End Date"]
    ).max()

    print("CURRENT END DATE =", current_end_date)
    print("MAX END DATE     =", max_end_date)

    if current_end_date != max_end_date:
        raise Exception(
            "Only active record can be revised."
        )

    effective_date = calculate_effective_date(
        request_date
    )

    print(
        "OLD RECORD END DATE =",
        format_date(request_date)
    )

    print(
        "NEW RECORD START DATE =",
        format_date(effective_date)
    )

    original_end_date = df.loc[
        row_index,
        "End Date"
    ]

    print(
        "TYPE OF ORIGINAL END DATE =",
        type(original_end_date)
    )

    print(
        "ORIGINAL END DATE =",
        original_end_date
    )

    new_row = df.loc[row_index].copy()

    df.loc[
        row_index,
        "End Date"
    ] = format_date(request_date)
    
    update_end_date(
        active_record["id"],
        request_date
    )

    new_row["Scenario"] = new_scenario
    new_row["CM Msgs"] = new_cm_msgs
    new_row["Fo Msgs"] = new_fo_msgs
    new_row["CD Msgs"] = new_cd_msgs
    new_row["Msg Line"] = new_msg_line
    new_row["Comments"] = new_comments

    new_row["Start Date"] = format_date(
        effective_date
    )

    if str(original_end_date).strip():

        parsed_end_date = parse_date(
            original_end_date
        )

        if pd.notna(parsed_end_date):

            parsed_end_date = parsed_end_date.date()

            if effective_date > parsed_end_date:

                month_end = get_month_end(
                    effective_date
                )

                new_row["End Date"] = format_date(
                    month_end
                )

                print(
                    "MONTH ROLLOVER DETECTED"
                )

                print(
                    "NEW MONTH END =",
                    new_row["End Date"]
                )

            else:

                new_row["End Date"] = format_date(
                    parsed_end_date
                )

        else:

            new_row["End Date"] = ""

    else:

        new_row["End Date"] = ""

    df = pd.concat(
        [df, pd.DataFrame([new_row])],
        ignore_index=True
    )

    print("OLD ROW UPDATED")
    print("NEW ROW CREATED")
    print(
        "TOTAL ROWS AFTER APPEND =",
        len(df)
    )

    print(
        "NEW ROW START =",
        new_row["Start Date"]
    )

    print(
        "NEW ROW END =",
        new_row["End Date"]
    )
    insert_new_record(new_row)
    
    cursor.close()
    connection.close()

    save_excel(df)

    return df

# ==========================================================
# FUNCTION : delete_latest_revision_record START
# ==========================================================
def delete_latest_revision_record(
    active_record
):

    print("DELETE REVISION STARTED")

    df = load_data()

    row_index = active_record.name

    exchange_ip = str(
        active_record["Exchange IP"]
    ).strip()

    ip_rows = df[
        df["Exchange IP"]
        .astype(str)
        .str.strip()
        ==
        exchange_ip
    ]
    ip_rows = ip_rows.copy()

    ip_rows["Start Date"] = pd.to_datetime(
        ip_rows["Start Date"],
        format="%d-%m-%Y",
        errors="coerce"
    )

    ip_rows = ip_rows.sort_values(
        by="Start Date"
    )

    print(
        "TOTAL REVISIONS =",
        len(ip_rows)
    )
    if len(ip_rows) < 2:

        raise Exception(
            "No previous revision found."
    )

    print("\nREVISION HISTORY")

    for idx, row in ip_rows.iterrows():

        print(
            idx,
            row["Start Date"],
            row["End Date"]
        )
    latest_row = ip_rows.iloc[-1]
    if latest_row.name != row_index:

        raise Exception(
            "Only latest active revision can be deleted."
    )

    previous_row = ip_rows.iloc[-2]
    print(
        "PREVIOUS END DATE =",
        previous_row["End Date"]
    )

    print(
        "LATEST END DATE =",
        latest_row["End Date"]
    )

    print(
        "LATEST INDEX =",
        latest_row.name
    )
    
    df.loc[
    previous_row.name,
    "End Date"
    ] = latest_row["End Date"]
    
    restore_end_date(
    int(previous_row["id"]),
    parse_date(latest_row["End Date"]).date()
)

    print(
        "PREVIOUS ROW RESTORED"
    )

    print(
        "NEW END DATE =",
        df.loc[
            previous_row.name,
            "End Date"
        ]
    )
    print(
        "TOTAL ROWS BEFORE DELETE =",
        len(df)
    )
    df = df.drop(
    index=latest_row.name
    )
    delete_record(
    int(latest_row["id"])
    )

    print(
        "TOTAL ROWS AFTER DELETE =",
        len(df)
    )
    save_excel(df)

    print(
        "DELETE REVISION COMPLETED"
    )

    return df

    print(
        "PREVIOUS INDEX =",
        previous_row.name
    )

    print(
        "ROW INDEX =",
        row_index
    )

    print(
        "EXCHANGE IP =",
        exchange_ip
    )
# ==========================================================
# FUNCTION : delete_latest_revision_record END
# ==========================================================