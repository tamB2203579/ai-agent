import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return (f"Error: Cannot write to '{file_path}' as it is outside the permitted working directory")

    if not os.path.exists(abs_file_path):
        f = open(abs_file_path, "w")
        
    try:
        with open(abs_file_path, "w") as f:
            is_success = f.write(content)
            if is_success:
                return (f"Successfully wrote to '{file_path}' ({len(content)} characters written)")
    except Exception as e:
        raise Exception(f"Error: {e}")
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write the provided content to the specified path, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the Python file to write, constrained to the working directory"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that will be written to the file_path, constrainted to the working directory"
            )
        }
    )
)