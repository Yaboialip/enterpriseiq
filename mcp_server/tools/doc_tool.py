import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from core.utils import success_response, error_response

def parse_document(filename: str, query: str = "") -> dict:
    """Parse PDF or Excel documents from the data folder."""
    filepath = os.path.join("data", filename)
    if not os.path.exists(filepath):
        return error_response(f"File '{filename}' not found in data folder.")
    try:
        text = ""
        if filename.endswith(".pdf"):
            import fitz
            doc = fitz.open(filepath)
            for page in doc:
                text += page.get_text()
            doc.close()
        elif filename.endswith((".xlsx", ".xls")):
            import openpyxl
            wb = openpyxl.load_workbook(filepath)
            for sheet in wb.worksheets:
                text += f"\n[Sheet: {sheet.title}]\n"
                for row in sheet.iter_rows(values_only=True):
                    text += " | ".join([str(c) for c in row if c is not None]) + "\n"
        elif filename.endswith(".txt"):
            with open(filepath, "r") as f:
                text = f.read()
        else:
            return error_response(f"Unsupported file type: {filename}")
        return success_response({
            "filename": filename,
            "content_length": len(text),
            "extracted_text": text[:4000]
        })
    except Exception as e:
        return error_response(str(e))