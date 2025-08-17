import os
from google.genai import types

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not abs_file_path.startswith(abs_working_dir):
            return (f"Error: Cannot read '{file_path}' as it is outside the permitted working directory")

        if not os.path.isfile(abs_file_path):
            return (f"Error: File not found or it not a regular file: '{file_path}'")

        with open(abs_file_path) as f:
            content = f.read()
            if len(content) >= MAX_CHARS:
                content = content[:10000] + f"[...File \"{file_path}\" truncated at 10000 characters]"
        return content
    except Exception as e:
        raise Exception(f"Error: {e}")

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="List the content of the file in the specified path, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file that need to get the content, relative to the working directory. If not provided, notify the user with error message"
            )
        }
    )    
)