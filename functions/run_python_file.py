import os
import subprocess
from google import genai
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working_directory = os.path.abspath(working_directory)
    abspath = os.path.abspath(os.path.join(working_directory, file_path))

    if not abspath.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abspath):
        return f'Error: File "{file_path}" not found.'


    if os.path.exists(abspath) and not abspath.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        command = ["python", abspath] + args

        completed_process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=abs_working_directory,
            timeout=30
        )

        stdout = completed_process.stdout.strip()
        stderr = completed_process.stderr.strip()

        result_parts = []
        if stdout:
            result_parts.append(f"STDOUT:\n{stdout}")
        if stderr:
            result_parts.append(f"STDERR:\n{stderr}")
        if completed_process.returncode != 0:
            result_parts.append(f"Process exited with code {completed_process.returncode}")

        if not result_parts:
            return "No output produced."

        return "\n".join(result_parts)

    except subprocess.TimeoutExpired:
        return f'Error: Execution timed out after 30 seconds'
    except Exception as e:
        return f"Error: executing Python file: {e}"



schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file from the working directory with optional arguments and returns its output or errors.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of command line argument to pass to the python file",
                items=types.Schema(type=types.Type.STRING)
            )
        },
        required=['file_path']
    ),
)

        