import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python
from functions.write_file import schema_write_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_file_content,
        schema_get_files_info,
        schema_run_python,
        schema_write_file
    ]
)

client = genai.Client(api_key=api_key)

user_prompt = sys.argv[1]
verbose = "--verbose" in sys.argv

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

for i in range(20):
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
        )

        for candidate in response.candidates:
            messages.append(candidate.content)

        if response.function_calls:
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose=verbose)

                if not hasattr(function_call_result, "parts") or len(function_call_result.parts) == 0:
                    raise RuntimeError(f"call_function returned invalid result: missing parts")
                
                if not hasattr(function_call_result.parts[0], "function_response") or not hasattr(function_call_result.parts[0].function_response, "response"):
                    raise RuntimeError(f"call_function returned invalid result: missing function_response.response")
                
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                
                messages.append(
                    types.Content(
                        role="user",
                        parts=[function_call_result.parts[0]]
                    )
                )
        elif response.text:
            print("Final response:")
            print(response.text)
            break
        
    except Exception as e:
        print(f"Error during loop iteration {i}: {e}")
        break