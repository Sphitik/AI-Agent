import os

def write_file(working_directory, file_path, content):
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
    try:
        with open(abspath , 'w') as f:
            f.write(content)
    except Exception as e:
        return f'{e}'

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    