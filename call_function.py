from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file_content import schema_write_file_content, write_file_content
from config import MAX_READ_CHARS 


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

def call_function(function_call_part, verbose=False):
    
    WORKING_DIRECTORY="./calculator"
    function_name = function_call_part.name
    kwargs = dict(function_call_part.args)

    # Optional logging
    if verbose:
        print(f"Calling function: {function_name}({kwargs})")
    else:
        print(f" - Calling function: {function_name}")
    

    if function_name not in FUNCTION_MAP:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"}
                )
            ]
        )

    kwargs["working_directory"] = WORKING_DIRECTORY
    function_result = FUNCTION_MAP[function_name](**kwargs)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )