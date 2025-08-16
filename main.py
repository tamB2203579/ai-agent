from email import message
import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

verbose = '--verbose' in sys.argv

user_prompt = sys.argv[1]

if verbose:
    print(f"User prompt: {user_prompt}")

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages
)
print(f"Gemini: {response.text}")

prompt_tokens = response.usage_metadata.prompt_token_count
candidate_tokens = response.usage_metadata.candidates_token_count

if verbose:
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {candidate_tokens}")
