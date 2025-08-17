from .get_file_content import get_file_content
from .get_files_info import get_files_info
from .run_python_file import run_python_file
from .write_file import write_file
from google.genai import types

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    args_dict = dict(function_call_part.args) if function_call_part.args else {}
    args_dict["working_directory"] = "./calculator"

    match function_call_part.name:
        case "get_file_content":
            result = get_file_content(**args_dict)
        case "get_files_info":
            result = get_files_info(**args_dict)
        case "run_python_file":
            result = run_python_file(**args_dict)
        case "write_file":
            result = write_file(**args_dict)
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"error": f"Unknown function: {function_call_part.name}"},
                    )
                ],
            )
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
            )
        ],
    )