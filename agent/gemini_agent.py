import google.generativeai as genai
import os, sys, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from core.config import GEMINI_API_KEY, MODEL_NAME
from mcp_server.tools.sql_tool import query_database
from mcp_server.tools.erp_tool import query_erp
from mcp_server.tools.doc_tool import parse_document

genai.configure(api_key=GEMINI_API_KEY)

# Load system prompt
PROMPT_PATH = os.path.join(os.path.dirname(__file__), "prompts/system_prompt.txt")
with open(PROMPT_PATH, "r") as f:
    SYSTEM_PROMPT = f.read()

# Tool definitions for Gemini function calling
TOOLS = [{
    "function_declarations": [
        {
            "name": "query_database",
            "description": "Query SQLite manufacturing database for inventory, production, machine data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sql_query": {"type": "string", "description": "SQL SELECT query to execute"}
                },
                "required": ["sql_query"]
            }
        },
        {
            "name": "query_erp",
            "description": "Query ERP system. query_type must be one of: orders, customers, suppliers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query_type": {"type": "string", "description": "Type: orders, customers, or suppliers"},
                    "status_filter": {"type": "string", "description": "Optional status filter"}
                },
                "required": ["query_type"]
            }
        },
        {
            "name": "parse_document",
            "description": "Parse PDF or Excel files from the data folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Filename in data/ folder"},
                    "query": {"type": "string", "description": "What to look for in document"}
                },
                "required": ["filename"]
            }
        }
    ]
}]

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    tools=TOOLS,
    system_instruction=SYSTEM_PROMPT
)

TOOL_MAP = {
    "query_database": query_database,
    "query_erp": query_erp,
    "parse_document": parse_document,
}

def chat(user_message: str, history: list = []) -> str:
    """Send message and handle tool calls automatically."""
    try:
        session = model.start_chat(history=history)
        response = session.send_message(user_message)

        # Handle tool calls in a loop
        max_iterations = 5
        iteration = 0
        while iteration < max_iterations:
            iteration += 1
            has_tool_call = False
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'function_call') and part.function_call.name:
                    has_tool_call = True
                    fn = part.function_call
                    args = dict(fn.args)
                    tool_fn = TOOL_MAP.get(fn.name)
                    if tool_fn:
                        result = tool_fn(**args)
                    else:
                        result = {"error": f"Unknown tool: {fn.name}"}
                    response = session.send_message(
                        genai.protos.Content(parts=[
                            genai.protos.Part(
                                function_response=genai.protos.FunctionResponse(
                                    name=fn.name,
                                    response={"result": json.dumps(result, default=str)}
                                )
                            )
                        ])
                    )
                    break
            if not has_tool_call:
                break

        return response.text
    except Exception as e:
        return f"Error: {str(e)}"