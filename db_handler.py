
import mysql.connector
from mysql.connector import pooling
import bcrypt
from date_utils import parse_date


from config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)
# ==========================================================
# MYSQL CONNECTION POOL
# ==========================================================

connection_pool = pooling.MySQLConnectionPool(

    pool_name="ctcl_pool",
    pool_size=10,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
def to_int(value):

    value = str(value).strip()

    if value == "":
        return 0

    return int(value)

# ==========================================================
# GET CONNECTION
# ==========================================================

def get_connection():

    connection = connection_pool.get_connection()

    return connection

def get_cursor():

    connection = get_connection()

    cursor = connection.cursor()

    return connection, cursor
def log_audit(
    username,
    module,
    action,
    description
):
    connection = None
    cursor = None

    try:
        connection, cursor = get_cursor()

        cursor.execute(
            """
            INSERT INTO audit_logs
            (
                username,
                module,
                action,
                description
            )
            VALUES
            (
                %s, %s, %s, %s
            )
            """,
            (
                username,
                module,
                action,
                description
            )
        )

        connection.commit()
    except Exception as e:
        print(f"Audit Log Error: {e}")

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

def hash_password(password):

    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def verify_password(
    password,
    password_hash
):

    return bcrypt.checkpw(
        password.encode(),
        password_hash.encode()
    )

def create_user(
    username,
    password,
    full_name,
    role,
    is_active
):

    connection, cursor = get_cursor()

    cursor.execute(
        """
        INSERT INTO users
        (
            username,
            password_hash,
            full_name,
            role,
            is_active
        )
        VALUES
        (
            %s,%s,%s,%s,%s
        )
        """,
        (
            username,
            hash_password(password),
            full_name,
            role,
            is_active
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    print("USER CREATED")
    
def update_user(
    username,
    full_name,
    role,
    is_active
):

    connection, cursor = get_cursor()

    cursor.execute(
        """
        UPDATE users
        SET
            full_name = %s,
            role = %s,
            is_active = %s
        WHERE username = %s
        """,
        (
            full_name,
            role,
            is_active,
            username
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    print("USER UPDATED")

def update_password(
    username,
    password
):

    connection, cursor = get_cursor()

    cursor.execute(
        """
        UPDATE users
        SET password_hash = %s
        WHERE username = %s
        """,
        (
            hash_password(password),
            username
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    print("PASSWORD UPDATED")
def disable_user_account(username):

    connection, cursor = get_cursor()

    cursor.execute(
        """
        UPDATE users
        SET is_active = 0
        WHERE username = %s
        """,
        (
            username,
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    print("USER DISABLED")
def delete_user_account(username):

    connection, cursor = get_cursor()

    cursor.execute(
        """
        DELETE FROM users
        WHERE username = %s
        """,
        (
            username,
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    print("USER DELETED")
def authenticate_user(
    username,
    password
):

    connection, cursor = get_cursor()

    cursor.execute(
        """
        SELECT
            password_hash,
            full_name,
            role
        FROM users
        WHERE username = %s
        AND is_active = 1
        """,
        (username,)
    )

    user = cursor.fetchone()

    print("DB USER =", user)

    cursor.close()
    connection.close()

    if user is None:
        print("USER NOT FOUND")
        return None

    password_hash, full_name, role = user

    print("HASH =", password_hash)

    result = verify_password(
        password,
        password_hash
    )

    print("PASSWORD MATCH =", result)

    if result:
        return {
            "username": username,
            "full_name": full_name,
            "role": role
        }

    return None

    connection, cursor = get_cursor()

    cursor.execute(
        """
        UPDATE ctcl_message_ratio
        SET end_date = %s
        WHERE id = %s
        """,
        (
            end_date,
            int(record_id)
        )
    )

    connection.commit()
    cursor.close()
    connection.close()

    print("MYSQL END DATE UPDATED")
    
def check_duplicate_ctcl(
    exchange_ip,
    fo_ctcl,
    cm_ctcl,
    cds_ctcl
):

    connection, cursor = get_cursor()

    cursor.execute(
        """
        SELECT id
        FROM ctcl_message_ratio
        WHERE
            exchange_ip = %s
            AND fo_ctcl = %s
            AND cm_ctcl = %s
            AND cds_ctcl = %s
        LIMIT 1
        """,
        (
            exchange_ip,
            fo_ctcl,
            cm_ctcl,
            cds_ctcl
        )
    )

    duplicate_record = cursor.fetchone()

    cursor.close()
    connection.close()

    return duplicate_record is not None
def insert_new_record(
    record
):

    connection, cursor = get_cursor()

    cursor.execute(
        """
        INSERT INTO ctcl_message_ratio
        (
            env,
            exchange_name,
            location,
            dedicated,
            system_name,
            server_ip,
            exchange_ip,
            fo_ctcl,
            cm_ctcl,
            cds_ctcl,
            dealer_id,
            rack,
            scenario,
            cm_msgs,
            fo_msgs,
            cd_msgs,
            msg_line,
            start_date,
            end_date,
            comments
        )
        VALUES
        (
            %s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s
        )
        """,
        (
            record["Env"],
            record["Exchange"],
            record["Location"],
            record["Dedicated"],
            record["System"],
            record["Server IP"],
            record["Exchange IP"],
            record["FO CTCL"],
            record["CM CTCL"],
            record["CDS CTCL"],
            record["Dealer ID"],
            record["Rack"],
            record["Scenario"],
            to_int(record["CM Msgs"]),
            to_int(record["Fo Msgs"]),
            to_int(record["CD Msgs"]),
            to_int(record["Msg Line"]),
            parse_date(record["Start Date"]).date(),
            parse_date(record["End Date"]).date(),
            record["Comments"]
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    print("MYSQL NEW RECORD INSERTED")

# ==========================================================
# UPDATE END DATE
# ==========================================================

def update_end_date(
    record_id,
    end_date
):

    connection, cursor = get_cursor()

    cursor.execute(
        """
        UPDATE ctcl_message_ratio
        SET end_date = %s
        WHERE id = %s
        """,
        (
            end_date,
            int(record_id)
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    print("MYSQL END DATE UPDATED")

def restore_end_date(
    record_id,
    end_date
):

    connection, cursor = get_cursor()

    cursor.execute(
        """
        UPDATE ctcl_message_ratio
        SET end_date = %s
        WHERE id = %s
        """,
        (
            end_date,
            int(record_id)
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    print("MYSQL END DATE RESTORED")


def delete_record(
    record_id
):

    connection, cursor = get_cursor()

    cursor.execute(
        """
        DELETE FROM ctcl_message_ratio
        WHERE id = %s
        """,
        (
            int(record_id),
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    print("MYSQL RECORD DELETED")
    
# ==========================================================
# GET ALL USERS
# ==========================================================

def get_all_users():

    connection, cursor = get_cursor()

    cursor.execute("""
        SELECT
            username,
            full_name,
            role,
            CASE
                WHEN is_active = 1 THEN 'Active'
                ELSE 'Disabled'
            END AS status
        FROM users
        ORDER BY username
    """)

    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return users
def get_active_admin_count():

    connection, cursor = get_cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM users
        WHERE role = 'Admin'
        AND is_active = 1
        """
    )

    count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return count

def user_exists(username):

    connection, cursor = get_cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM users
        WHERE username = %s
        """,
        (
            username,
        )
    )

    count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return count > 0
# ==========================================================
# DASHBOARD STATISTICS
# ==========================================================

def get_total_records():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM ctcl_message_ratio"
    )

    total = cursor.fetchone()[0]

    cursor.close()

    connection.close()

    return total


def get_active_records():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM ctcl_message_ratio

        WHERE end_date >= CURDATE()

    """)

    total = cursor.fetchone()[0]

    cursor.close()

    connection.close()

    return total


def get_total_users():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(

        "SELECT COUNT(*) FROM users"

    )

    total = cursor.fetchone()[0]

    cursor.close()

    connection.close()

    return total


def get_total_revisions():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM ctcl_message_ratio
        WHERE start_date < CURDATE()
        """
    )

    total = cursor.fetchone()[0]

    cursor.close()

    connection.close()

    return total


# ==========================================================
# RECENT REVISIONS
# ==========================================================

def get_recent_revisions():

    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            exchange_ip,
            scenario,
            DATE_FORMAT(start_date, '%d-%m-%Y') AS start_date,
            comments
        FROM ctcl_message_ratio
        ORDER BY start_date DESC
        LIMIT 5
        """
    )

    records = cursor.fetchall()

    cursor.close()
    connection.close()

    return records
def get_record_by_id(record_id):

    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM ctcl_message_ratio
        WHERE id = %s
        """,
        (
            record_id,
        )
    )

    record = cursor.fetchone()

    cursor.close()
    connection.close()

    return record

# ==========================================================
# SEARCH RECORDS
# ==========================================================

def search_records_db(
    search_type,
    search_value
):

    column_mapping = {

        "Exchange IP": "exchange_ip",
        "FO CTCL": "fo_ctcl",
        "CM CTCL": "cm_ctcl",
        "CDS CTCL": "cds_ctcl",
        "Dealer ID": "dealer_id"

    }

    db_column = column_mapping.get(search_type)

    if db_column is None:

        raise Exception(
            f"Invalid search type: {search_type}"
        )

    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    query = f"""
        SELECT *
        FROM ctcl_message_ratio
        WHERE {db_column} = %s
        ORDER BY end_date DESC
    """

    cursor.execute(
        query,
        (search_value,)
    )

    records = cursor.fetchall()

    cursor.close()
    connection.close()

    print("Searching :", search_type, search_value)
    print("DB Column :", db_column)
    print("Records Found :", len(records))

    return records
def get_revision_history(exchange_ip):

    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            id,
            exchange_ip,
            start_date,
            end_date
        FROM ctcl_message_ratio
        WHERE exchange_ip = %s
        ORDER BY start_date
        """,
        (
            exchange_ip,
        )
    )

    records = cursor.fetchall()

    print("REVISION HISTORY =", records)
    print("TOTAL REVISIONS =", len(records))

    cursor.close()
    connection.close()

    return records
# ==========================================================
# GET USER BY USERNAME
# ==========================================================

def get_user_by_username(
    username
):

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    cursor.execute(
        """
        SELECT
            username,
            full_name,
            role,
            is_active
        FROM users
        WHERE username = %s
        """,
        (
            username,
        )
    )

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return user
# ==========================================================
# INSERT AUDIT LOG
# ==========================================================

# ==========================================================
# INSERT AUDIT LOG
# ==========================================================

def insert_audit_log(

    username,
    source,
    module,
    action,
    description

):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(

        """
        INSERT INTO audit_logs
        (

            username,
            source,
            module,
            action,
            description

        )

        VALUES

        (

            %s,
            %s,
            %s,
            %s,
            %s

        )
        """,

        (

            username,
            source,
            module,
            action,
            description

        )

    )

    connection.commit()

    cursor.close()

    connection.close()

    print("AUDIT LOG INSERTED")
    
# ==========================================================
# GET AUDIT LOGS
# ==========================================================

def get_audit_logs():

    connection = get_connection()

    cursor = connection.cursor(

        dictionary=True

    )

    cursor.execute(

        """
        SELECT

            username,
            source,
            module,
            action,
            description,

            DATE_FORMAT(
                created_at,
                '%d-%m-%Y %H:%i:%s'
            ) AS created_at

        FROM audit_logs

        ORDER BY id DESC

        """

    )

    logs = cursor.fetchall()

    cursor.close()

    connection.close()

    return logs
