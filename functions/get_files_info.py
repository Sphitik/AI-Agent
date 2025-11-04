import os
from config import MAX_READ_CHARS
def get_files_info(working_directory, directory="."):

    abs_working_directory=os.path.abspath(working_directory)
    abspath = os.path.abspath(os.path.join(working_directory, directory))
    
    if not abspath.startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(abspath):
        return f'Error: "{directory}" is not a directory'

    info_list=[]
    try:
        for file in os.listdir(abspath):
            file_path = os.path.join(abspath,file)
            info_list.append(f'- {file}: file_size={os.path.getsize(file_path)}, is_dir={os.path.isdir(file_path)}')
        
        return ('\n').join(info_list)
    except Exception as e:
        return "Error listing files: {e}"
    
 
