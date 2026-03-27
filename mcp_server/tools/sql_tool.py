import sqlite3
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from core.config import DB_PATH
from core.utils import success_response, error_response

def query_database(sql_query: str) -> dict:
    """Query SQLite manufacturing database."""
    try:
        # Safety check - only allow SELECT
        if not sql_query.strip().upper().startswith("SELECT"):
            return error_response("Only SELECT queries are allowed.")
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return success_response(rows, len(rows))
    except Exception as e:
        return error_response(str(e))