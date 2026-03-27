import json
from datetime import datetime

def success_response(data, rows=None):
    result = {"status": "success", "data": data}
    if rows is not None:
        result["rows"] = rows
    return result

def error_response(message):
    return {"status": "error", "message": message}

def format_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")