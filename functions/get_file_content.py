import os

MAX_CHARS = 10000

def get_files_content(working_directory, file_path):
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
