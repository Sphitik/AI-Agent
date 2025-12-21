from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file_content import schema_write_file_content, write_file_content
from config import MAX_READ_CHARS 
import json


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file_content,
    ]
)
 
FUNCTION_MAP = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file_content": write_file_content,
}

def safe_json(value):
    """Ensure the function result is JSON-serializable."""
    try:
        json.dumps(value)
        return value
    except Exception:
        return str(value)


def call_function(function_call_part, verbose=False):
    name = function_call_part.name
    args = function_call_part.args.to_dict() if function_call_part.args else {}

    # Force working directory
    args["working_directory"] = "./calculator"

    if name not in FUNCTION_MAP:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"error": f"Unknown function: {name}"},
                )
            ],
        )

    try:
        result = FUNCTION_MAP[name](**args)
    except Exception as e:
        result = f"Error calling function: {e}"

    result = safe_json(result)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=name,
                response={"result": result},
            )
        ],
    )
