import os
from google import genai
from google.genai import types

def write_file_content(working_directory, file_path, content):
    abs_working_directory= os.path.abspath(working_directory)
    abspath=os.path.abspath(os.path.join(working_directory, file_path))

    directory= os.path.dirname(abspath)

    if not abspath.startswith(abs_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        if directory:
            os.makedirs(directory, exist_ok=True)
    except Exception as e:
        return f'Error making directory: {e}'
    
    if os.path.exists(abspath) and os.path.isdir(abspath):
        return f'Error: "{file_path}" is a directory, not a file'
    
    try:
        with open(abspath , 'w') as f:
            f.write(content)
    except Exception as e:
        return f'{e}'

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'



schema_write_file_content = types.FunctionDeclaration(
    name="write_file_content",
    description="Writes or overwrites a file in the working directory with the provided text content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)
  