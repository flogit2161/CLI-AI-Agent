import os 
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes Python files with optional arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to run files from, relative to the working directory. If not provided, run files in the working directory itself.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(working_directory)
    abs_path_target = os.path.abspath(full_path)
    
    inside = (
        abs_path == abs_path_target or
        abs_path_target.startswith(abs_path + os.sep)
    )
    if not inside:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    if not full_path.endswith('.py'):   
        return f'Error: "{file_path}" is not a Python file'
    
    cmd = ['python', file_path] + list(map(str, args))
    
    try:
        completed_process = subprocess.run(cmd, capture_output=True, cwd=working_directory, timeout=30, check=False, text=True)
        code = completed_process.returncode
        stdout = completed_process.stdout 
        stderr = completed_process.stderr

        if not stdout.strip() and not stderr.strip():
            return 'No output produced.'
        parts = []
        if stdout:
            parts.append(f"STDOUT: {stdout}".rstrip())
        if stderr:
            parts.append(f"STDERR: {stderr}".rstrip())
        if code != 0:
            parts.append(f"Process exited with code {code}")

        return "\n".join(parts)
        
    except Exception as e:
        return f'Error: executing Python file: {e}'
