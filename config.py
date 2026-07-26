import os
from pathlib import Path
from dotenv import load_dotenv

# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

# ==========================================================
# APPLICATION CONFIGURATION
# ==========================================================

EXCEL_FILE = (
    r"C:\Users\Mahtab\Documents\CTCL_TOOL\data\CTCL-Jul-2026.xlsx"
)

BACKUP_FOLDER = "backup"

APP_NAME = "CTCL Message Ratio Management Tool"

APP_VERSION = "1.0"

# ==========================================================
# MYSQL CONFIGURATION
# ==========================================================

DB_HOST = os.getenv("DB_HOST")

DB_PORT = int(os.getenv("DB_PORT", 3306))

DB_NAME = os.getenv("DB_NAME")

DB_USER = os.getenv("DB_USER")

DB_PASSWORD = os.getenv("DB_PASSWORD")

# ==========================================================
# APPLICATION SECRET
# ==========================================================

SECRET_KEY = os.getenv("SECRET_KEY")