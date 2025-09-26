import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite files.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            'file_path': types.Schema(
                type=types.Type.STRING,
                description='Path to the file, relative to working directory'
            ),
            'content': types.Schema(
                type=types.Type.STRING,
                description= 'Text content to write to the file'
            )
        },
        required=['file_path', 'content']
    ),
)

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(working_directory)
    abs_path_target = os.path.abspath(full_path)
    
    inside = (
        abs_path == abs_path_target or
        abs_path_target.startswith(abs_path + os.sep)
    )
    if not inside:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)            
        with open(full_path, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'

        
            