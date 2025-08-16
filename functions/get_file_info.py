import os
from urllib.parse import _ResultMixinStr

def get_files_info(working_directory, directory="."):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_target_path = os.path.abspath(os.path.join(working_directory, directory))

        if not abs_target_path.startswith(abs_working_directory):
            return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        
        if not os.path.isdir(abs_target_path):
            return (f"Error: {directory} is not a directory")

        result = ""
        result += f"Result for {directory} directory:\n"
        for item in os.listdir(abs_target_path):
            item_path = os.path.join(abs_target_path, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            result += f" -{item}: file_size={file_size} bytes, is_dir={is_dir}\n"
        return result
    except Exception as e:
        print(f"Error: {e}")
        