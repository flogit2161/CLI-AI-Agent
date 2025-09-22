import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    abs_path = os.path.abspath(working_directory)
    abs_path_target = os.path.abspath(full_path)
    
    inside = (
        abs_path == abs_path_target or
        abs_path_target.startswith(abs_path + os.sep)
    )
    if not inside:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
   
    files_results = os.listdir(full_path)
    entries = []
    try:

        for file in files_results:
            entry_path = os.path.join(full_path, file)
            file_size = os.path.getsize(entry_path)
            valid_dir = os.path.isdir(entry_path)
            entries.append(f'-{file}: file_size={file_size}, is_dir={valid_dir}')
        return '\n'.join(entries)
    except Exception as e:
        return f'Error:{e}'