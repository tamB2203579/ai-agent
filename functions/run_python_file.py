import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        completed_process = subprocess.run(
            ["python3", abs_file_path] + args,
            capture_output=True,
            text=True,
            timeout=30
        )
        stdout = completed_process.stdout.strip()
        stderr = completed_process.stderr.strip()
        output = []

        if stdout:
            output.append(f"STDOUT: {stdout}")
        if stderr:
            output.append(f"STDERR: {stderr}")
        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")
        if not output:
            return "No output produced."
        
        return "\n".join(output)
    except subprocess.TimeoutExpired:
        return "Error: Execution timed out after 30 seconds."
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within a specified working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the Python file to execute, constrained to the working directory."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="A list of arguments to pass to the Python file during execution.",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="An individual argument to pass to the Python file."
                )
            )
        }
    )
)