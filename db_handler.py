
import mysql.connector
import bcrypt
from date_utils import parse_date


from config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)
def to_int(value):

    value = str(value).strip()

    if value == "":
        return 0

    return int(value)

def get_connection():

    print(
        "CONNECTING TO MYSQL..."
    )
    print("CONNECTING TO:")
    print("HOST =", DB_HOST)
    print("PORT =", DB_PORT)
    print("DATABASE =", DB_NAME)

    connection = mysql.connector.connect(

        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD

    )

    print(
        "MYSQL CONNECTED"
    )

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

def update_end_date(
    record_id,
    end_date
):
#     print("INSERT_NEW_RECORD FUNCTION CALLED")
#     print(record)
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


    