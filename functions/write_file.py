import os

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