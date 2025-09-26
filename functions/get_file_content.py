import os 
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read files contents.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath to read files from, relative to the working directory.",
            ),
        },
        required= ['file_path']
    ),
)


def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(working_directory)
    abs_path_target = os.path.abspath(full_path)
    
    inside = (
        abs_path == abs_path_target or
        abs_path_target.startswith(abs_path + os.sep)
    )
    if not inside:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(full_path, 'r') as f:
            file_content_string = f.read(MAX_CHARS+1)
    except Exception as e:
            return f'Error: {e}'
    
    if len(file_content_string) > MAX_CHARS:
        truncated_text = file_content_string[:MAX_CHARS]
        return truncated_text + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    else:
        return file_content_string
        
        