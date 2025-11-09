import os
from google import genai
from google.genai import types
from config import MAX_READ_CHARS

def get_file_content(working_directory, file_path):
    abs_working_directory=os.path.abspath(working_directory)
    abspath = os.path.abspath(os.path.join(working_directory, file_path))

    if not abspath.startswith(abs_working_directory):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abspath):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(abspath,"r") as f:
            text=f.read(MAX_READ_CHARS + 1)
            if len(text) < MAX_READ_CHARS:
                return text
            else:
                truncated=text[:MAX_READ_CHARS]
                return f'{truncated} [...File "{file_path}" truncated at 10000 characters]'
    except Exception as e:
        return f'Error: {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read and returns the contents of the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory",
            ),
        },
        required=['file_path']
    ),
)
